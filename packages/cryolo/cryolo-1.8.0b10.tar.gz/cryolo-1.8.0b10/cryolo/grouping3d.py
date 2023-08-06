import numpy as np
from cryolo import  utils

def convert_traces_to_bounding_boxes(traces):
    """
    Converts traces to a list of BoundingBox instances
    :param traces: Results of tracing
    :return: List of BoundingBox instances.
    """
    ccords = []
    for trace_id in np.unique(traces["particle"]):#range(num_particles):
        one_trace = traces[traces["particle"] == trace_id]

        xcoords = one_trace["x"].tolist()
        ycoords = one_trace["y"].tolist()
        zcoords = one_trace["frame"].tolist()
        widths = one_trace["widths"].tolist()
        heights = one_trace["heights"].tolist()
        confidence = one_trace["confidence"].tolist()
        est_box_widths = [meta["boxsize_estimated"][0] for meta in one_trace["meta"].tolist()]
        est_box_heights = [meta["boxsize_estimated"][1] for meta in one_trace["meta"].tolist()]

        x = np.mean(xcoords)
        y = np.mean(ycoords)
        z = np.round(np.mean(zcoords))
        w = np.mean(widths)
        h = np.mean(heights)
        c = np.mean(confidence)
        estimated_boxsize = (np.mean(est_box_widths),np.mean(est_box_heights))

        meta = {"boxsize_estimated": estimated_boxsize}
        meta["num_boxes"] = len(xcoords)
        bbox = utils.BoundBox(
            x=x,
            y=y,
            z=z,
            c=c,
            w=w,
            h=h,
            depth=w, # set it to same as the width. Should be a cube anyway.
            classes=[c]
        )
        bbox.meta = meta
        ccords.append(bbox)
    return ccords

def do_tracing(boxes_list,
               search_range=5,
               memory=3,
               confidence_threshold=0,
               min_length=5):
    """
    Will trace the boxes

    :param boxes_list: List of BoundingBox instances
    :param search_range: Maximum distance between position to get linked
    :param memory: Maximum gap in z direction.
    :param min_length: Minimum trace length (default 5)
    :return: List of coordinates (x,y,z,c) where c is the confidence. x,y,z are center coordinates.
    """
    import pandas as pd
    import trackpy as tp
    coords_and_frame = {"x": [], "y": [], "frame": []}
    confidences = []
    meta = []
    widths = []
    heights = []
    for boxes_index, boxes in enumerate(boxes_list):
        for box in boxes:
            if box.c > confidence_threshold:
                coords_and_frame["x"].append(box.x)
                coords_and_frame["y"].append(box.y)
                coords_and_frame["frame"].append(boxes_index)
                confidences.append(box.c)
                meta.append(box.meta)
                widths.append(box.w)
                heights.append(box.h)
                assert len(box.classes) == 1, "for classes > 1 we need to complete the implementation"
    coords_frame_df = pd.DataFrame(coords_and_frame)

    tp.quiet(True)
    coords_frame_traced_df = tp.link_df(coords_frame_df,
                                       search_range=search_range,
                                       memory=memory)
    coords_frame_traced_df["confidence"] = confidences
    coords_frame_traced_df["meta"] = meta
    coords_frame_traced_df["widths"] = widths
    coords_frame_traced_df["heights"] = heights
    coords_frame_traced_df= tp.filter_stubs(coords_frame_traced_df, min_length)
    boxes = convert_traces_to_bounding_boxes(coords_frame_traced_df)
    return boxes

def do_cluster(boxes_list,max_dist=2,max_z=3, confidence_threshold=0.3):

    num_boxes = np.sum([len([box for box in boxes if box.c>confidence_threshold]) for boxes in boxes_list])

    data = np.zeros(shape=(num_boxes,3))
    k = 0
    for boxes_index, boxes in enumerate(boxes_list):
        for box in boxes:
            if box.c > confidence_threshold:
                data[k,0]=box.x
                data[k,1]=box.y
                data[k,2]=boxes_index
                k = k + 1
    from sklearn import cluster
    epsilon = np.sqrt(max_dist * max_dist + max_z * max_z)

    clustering = cluster.AgglomerativeClustering(n_clusters=None, distance_threshold=80).fit(data) #cluster.DBSCAN(eps=epsilon, min_samples=3).fit(data)

    print("Num clusters found:", len(set(clustering.labels_)))

    return None#NotImplementedError("This method is not implemented yet")
