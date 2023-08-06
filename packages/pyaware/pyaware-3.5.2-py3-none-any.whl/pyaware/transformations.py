from copy import deepcopy
import ruamel.yaml


def scale_values(definition: dict):
    def scaled(data: dict):
        """
        Scales the input data dictionary based on a definition dictionary. If the parameter in data is not present in
        the definition then it is skipped i.e. still included in the output dictionary just not scaled.

        :param definition: Dictionary in the form -> {"param1": scale_factor, "param2": scale_factor, ...}
        :param data: Dictionary to be altered in the form -> {"param1": data, "param2": data, ...}
        :return: Data dictionary with specified parameters scaled in the form ->
                {"param1": scaled_data, "param2": scaled_data, ...}
        """
        intersect = data.keys() & definition.keys()
        return {k: data[k] * definition[k] if k in intersect else data[k] for k in data}

    return scaled


def rename_keys(keys):
    def renamed(d):
        """
        Return a new dictionary with the keys renamed. If the key does not exist in the input data, this is skipped
        i.e. still included in the output dictionary just not renamed.

        :param keys: Input key renaming definition in the form -> {"key_to_be_renamed": "new_key_id", ...}
        :param d: Data dictionary to be renamed in the form -> {"key_to_be_renamed": data, ...}
        :return: Data dictionary with specified parameters renamed in the form -> {"new_key_id": data, ...}
        """
        if isinstance(d, dict):
            d = deepcopy(d)
            for k, v in keys.items():
                try:
                    d[v] = d.pop(k)
                except:
                    pass
            return d
        return d

    return renamed


def multiply_params(definition: dict):
    def multiplied(data: dict):
        """
        Multiplies defined parameters together on the defined key. If the key does not exist in the input data,
        this is skipped i.e. still included in the output dictionary just not altered.

        :param definition: Dictionary in the form -> {"param_name": ["param_name", "param2_name", ...], ...}
        :param data: Data dicitonary to have the multiplications applied in the form ->
                    {"param_name": value1, "param2_name": value2, ...}
        :return: Data dicitionary with the specified parameters multiplied in the form ->
                    {"param_name": value1 * value2 * ..., "param2_name": value2, ...}
        """
        for param, param_arr in definition.items():
            value = 1
            try:
                for p in param_arr:
                    value *= data[p]
                data[param] = value
            except KeyError:
                continue
        return data

    return multiplied


def remove_keys(definition: list):
    def removed(data: dict):
        """
        Remove keys from data dictionary based on a definition supplied. If the key does not exist in the input data,
        this is skipped i.e. still included in the output dictionary just not removed.

        :param definition: Input key removing definition in the form -> ["key_to_be_removed", ...]
        :param data: Data dictionary to be removed in the form -> {"key_to_be_removed": data, ...}
        :return: Data dictionary with the specified parameters removed.
        """
        d = deepcopy(data)
        for k in definition:
            d.pop(k, None)
        return d

    return removed


transforms = {
    "scale_values": scale_values,
    "rename_keys": rename_keys,
    "multiply_params": multiply_params,
    "remove_keys": remove_keys,
}


def transform(data: dict, transformations: list):
    """
    Transform data dictionary with the given list of transformations.

    :param data: Data dictionary to be transformed in the form -> {"param1": data, "param2": data, ...}
    :param transformations: List of transformations to be performed in the form -> [tx1(def), tx2(def), ...]
    :return: Transformed data dictionary -> {"param1": data, "param2": data, ...}
    """
    for tx in transformations:
        data = tx(data)
    return data


def build_from_device_config(path):
    """
    Builds the transformations from a configuration file
    :param path:
    :return:
    """
    with open(path) as f:
        parsed = ruamel.yaml.safe_load(f)
    transformations = []
    for t in parsed["transformations"]:
        for tx, data in t.items():
            try:
                definition = data["definition"]
            except KeyError:
                continue
            transformations.append(transforms[tx](definition))
    return transformations
