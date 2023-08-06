import argparse
import os
import json
import shutil

import requests
import cv2
import numpy as np

from collections import defaultdict
from pycocotools.coco import COCO
from panopticapi.utils import id2rgb
from tqdm import tqdm


# Returns unique values of list. Values can be dicts or lists!
def dict_setter(list_of_dicts):
    return [
        d for n, d in enumerate(list_of_dicts) if d not in list_of_dicts[n + 1:]
    ]


def _rle_to_polygon(coco_json, annotation):
    coco = COCO(coco_json)
    binary_mask = coco.annToMask(annotation)
    contours, hierarchy = cv2.findContours(
        binary_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    segmentation = []

    for contour in contours:
        contour = contour.flatten().tolist()
        if len(contour) > 4:
            segmentation.append(contour)
        if len(segmentation) == 0:
            continue
    return segmentation


def coco_instance_segmentation_to_sa_vector(coco_path, images_path):
    coco_json = json.load(open(coco_path))
    image_id_to_annotations = {}
    cat_id_to_cat = {}
    for cat in coco_json['categories']:
        cat_id_to_cat[cat['id']] = cat

    for annot in tqdm(coco_json['annotations'], "Converting annotations"):
        if 'iscrowd' in annot and annot['iscrowd'] == 1:
            try:
                annot['segmentation'] = _rle_to_polygon(coco_path, annot)
            except IndexError:
                print("List index out of range")

        cat = cat_id_to_cat[annot['category_id']]
        sa_dict_bbox = {
            'type': 'bbox',
            'points':
                {
                    'x1': annot['bbox'][0],
                    'y1': annot['bbox'][1],
                    'x2': annot['bbox'][0] + annot['bbox'][2],
                    'y2': annot['bbox'][1] + annot['bbox'][3]
                },
            'className': cat['name'],
            'classId': cat['id'],
            'attributes': [],
            'probability': 100,
            'locked': False,
            'visible': True,
            'groupId': annot['id'],
            'imageId': annot['image_id']
        }

        sa_polygon_loader = [
            {
                'type': 'polygon',
                'points': polygon,
                'className': cat['name'],
                'classId': cat['id'],
                'attributes': [],
                'probability': 100,
                'locked': False,
                'visible': True,
                'groupId': annot['id'],
                'imageId': annot['image_id']
            } for polygon in annot['segmentation']
        ]

        for polygon in sa_polygon_loader:
            if polygon['imageId'] not in image_id_to_annotations:
                image_id_to_annotations[polygon['imageId']] = [polygon]
            else:
                image_id_to_annotations[polygon['imageId']].append(polygon)
            if sa_dict_bbox['imageId'] not in image_id_to_annotations:
                image_id_to_annotations[sa_dict_bbox['imageId']] = [
                    sa_dict_bbox
                ]
            else:
                image_id_to_annotations[sa_dict_bbox['imageId']
                                       ].append(sa_dict_bbox)

    sa_jsons = {}
    for img in tqdm(coco_json['images'], "Writing annotations to disk"):
        if img['id'] not in image_id_to_annotations:
            continue
        f_loader = image_id_to_annotations[img['id']]
        if 'file_name' in img:
            image_path = img['file_name']
        else:
            image_path = img['coco_url'].split('/')[-1]
        file_name = image_path + "___objects.json"
        sa_jsons[file_name] = f_loader
    return sa_jsons


def coco_keypoint_detection_to_sa_vector(coco_path, images_path):
    coco_json = json.load(open(coco_path))
    loader = []

    cat_id_to_cat = {}
    for cat in coco_json["categories"]:
        cat_id_to_cat[cat["id"]] = {
            "name": cat["name"],
            "keypoints": cat["keypoints"],
            "skeleton": cat["skeleton"]
        }

    for annot in coco_json['annotations']:
        if annot['num_keypoints'] > 0:
            sa_points = [
                item for index, item in enumerate(annot['keypoints'])
                if (index + 1) % 3 != 0
            ]

            for n, i in enumerate(sa_points):
                if i == 0:
                    sa_points[n] = -17
            sa_points = [
                (sa_points[i], sa_points[i + 1])
                for i in range(0, len(sa_points), 2)
            ]

            if annot["iscrowd"] == 1:
                annot["segmentation"] = _rle_to_polygon(annot)

            if annot["category_id"] in cat_id_to_cat.keys():
                keypoint_names = cat_id_to_cat[annot["category_id"]
                                              ]['keypoints']

                sa_dict_bbox = {
                    'type': 'bbox',
                    'points':
                        {
                            'x1': annot['bbox'][0],
                            'y1': annot['bbox'][1],
                            'x2': annot['bbox'][0] + annot['bbox'][2],
                            'y2': annot['bbox'][1] + annot['bbox'][3]
                        },
                    'className': cat_id_to_cat[annot["category_id"]]["name"],
                    'classId': annot["category_id"],
                    'pointLabels': {},
                    'attributes': [],
                    'probability': 100,
                    'locked': False,
                    'visible': True,
                    'groupId': annot['id'],
                    'imageId': annot['image_id']
                }

                sa_polygon_loader = [
                    {
                        'type':
                            'polygon',
                        'points':
                            polygon,
                        'className':
                            cat_id_to_cat[annot["category_id"]]["name"],
                        'classId':
                            annot["category_id"],
                        'pointLabels': {},
                        'attributes': [],
                        'probability':
                            100,
                        'locked':
                            False,
                        'visible':
                            True,
                        'groupId':
                            annot['id'],
                        'imageId':
                            annot['image_id']
                    } for polygon in annot['segmentation']
                ]

                sa_template = {
                    'type': 'template',
                    'classId': annot['category_id'],
                    'probability': 100,
                    'points': [],
                    'connections': [],
                    'attributes': [],
                    'attributeNames': [],
                    'groupId': annot['id'],
                    'pointLabels': {},
                    'locked': False,
                    'visible': True,
                    'templateId': -1,
                    'className': cat_id_to_cat[annot["category_id"]]["name"],
                    'templateName': 'skeleton',
                    'imageId': annot['image_id']
                }

                for kp_name in keypoint_names:
                    pl_key = keypoint_names.index(kp_name)
                    sa_template['pointLabels'][pl_key] = kp_name

                for connection in cat_id_to_cat[annot["category_id"]
                                               ]['skeleton']:
                    index = cat['skeleton'].index(connection)
                    sa_template['connections'].append(
                        {
                            'id':
                                index + 1,
                            'from':
                                cat_id_to_cat[annot["category_id"]]['skeleton']
                                [index][0],
                            'to':
                                cat_id_to_cat[annot["category_id"]]['skeleton']
                                [index][1]
                        }
                    )

                for point_index, point in enumerate(sa_points):
                    if sa_points[point_index] == (-17, -17):
                        x = 5
                        y = 5
                    else:
                        x = sa_points[point_index][0],
                        y = sa_points[point_index][1]

                    sa_template['points'].append(
                        {
                            'id': point_index + 1,
                            'x': x,
                            'y': y
                        }
                    )

                for img in coco_json['images']:
                    for polygon in sa_polygon_loader:
                        if polygon['imageId'] == img['id']:
                            loader.append((img['id'], polygon))
                        if sa_dict_bbox['imageId'] == img['id']:
                            loader.append((img['id'], sa_dict_bbox))
                        if sa_template['imageId'] == img['id']:
                            loader.append((img['id'], sa_template))

        sa_jsons = {}
        for img in coco_json['images']:
            f_loader = []
            for img_id, img_data in loader:
                if img['id'] == img_id:
                    f_loader.append(img_data)
            file_name = img['file_name'] + "___objects.json"
            sa_jsons[file_name] = f_loader
    return sa_jsons