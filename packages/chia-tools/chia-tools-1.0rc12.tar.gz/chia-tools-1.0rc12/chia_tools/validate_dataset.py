from chia import instrumentation
from chia.components.datasets import DatasetFactory
from chia.components.datasets.dataset import Dataset
from chia import knowledge

import unittest
import functools
import networkx as nx
from tqdm import tqdm

import argparse


def validate(config: dict, deep: bool):
    observer = instrumentation.ObserverFactory.create(config={"name": "stream"})
    obs = instrumentation.NamedObservable("validate_dataset")
    obs.register(observer)

    print("Instantiating dataset")
    dataset: Dataset = DatasetFactory.create(config=config, observers=[observer])

    setups = dataset.setups()
    print(f"Testing {len(setups)}")
    for i, setup in enumerate(setups):
        print(f"Loading setup {i + 1} of {len(setups)}")
        validate_setup(dataset, setup, observers=[observer], deep=deep)


def validate_setup(dataset: Dataset, setup, observers, deep):
    dataset.setup(**setup)

    tc = unittest.TestCase()

    # Data
    train_pool_count = dataset.train_pool_count()
    test_pool_count = dataset.test_pool_count()
    tc.assertGreater(train_pool_count, 0, "There are train pools")
    tc.assertGreater(test_pool_count, 0, "There are test pools")
    tc.assertIsNotNone(dataset.namespace())

    train_sample_uids = [set()] * train_pool_count
    test_sample_uids = [set()] * test_pool_count

    # Examine pools individually
    all_concept_uids = set()
    for train_pool_index in range(train_pool_count):
        print(f"Testing train pool {train_pool_index + 1} of {train_pool_count}")
        train_pool = dataset.train_pool(train_pool_index, "label_gt")
        tc.assertGreater(len(train_pool), 0, "Train pool is not empty")

        for sample in tqdm(train_pool):
            validate_sample(tc, dataset, sample, deep)
            all_concept_uids |= {sample.get_resource("label_gt")}
            train_sample_uids[train_pool_index] |= {sample.get_resource("uid")}

    for test_pool_index in range(test_pool_count):
        print(f"Testing test pool {test_pool_index + 1} of {test_pool_count}")
        test_pool = dataset.test_pool(test_pool_index, "label_gt")
        tc.assertGreater(len(test_pool), 0, "Test pool is not empty")

        for sample in tqdm(test_pool):
            validate_sample(tc, dataset, sample, deep)
            all_concept_uids |= {sample.get_resource("label_gt")}
            test_sample_uids[test_pool_index] |= {sample.get_resource("uid")}

    # Train / test intersection
    all_train_uids = functools.reduce(lambda x, y: x | y, train_sample_uids, set())
    all_test_uids = functools.reduce(lambda x, y: x | y, test_sample_uids, set())

    train_test_intersection = all_train_uids.intersection(all_test_uids)

    tc.assertTrue(
        len(train_test_intersection) == 0, "Train and test set have no intersection"
    )

    # Relation
    tc.assertIsNotNone(
        dataset.get_hyponymy_relation_source(), "Dataset provides a hypernymy relation"
    )

    # Compare all_concept_uids to prediction targets
    prediction_target_uids = set(dataset.prediction_targets())
    for prediction_target_uid in prediction_target_uids:
        tc.assertIn(
            prediction_target_uid,
            all_concept_uids,
            "Dataset reports prediction targets correctly",
        )

    # Try constructing a knowledge base
    kb = knowledge.KnowledgeBaseFactory.create(dict(), observers=observers)
    kb.add_prediction_targets(dataset.prediction_targets())
    relation_sources = [dataset.get_hyponymy_relation_source()]
    relation_sources += [knowledge.WordNetAccess()]

    kb.add_hyponymy_relation(relation_sources)

    rgraph: nx.DiGraph = kb.get_hyponymy_relation_rgraph()
    possible_roots = [node for node in rgraph.nodes if rgraph.in_degree(node) == 0]
    tc.assertEqual(1, len(possible_roots), "There should be only one root.")
    root = next(nx.topological_sort(rgraph))

    for uid in all_concept_uids:
        # The root is fine
        if uid == root:
            continue

        tc.assertTrue(
            nx.has_path(rgraph, root, uid),
            f"The UID {uid} should be connected to the root {root}.",
        )


def validate_sample(tc, dataset, sample, deep):
    tc.assertTrue(
        str(sample.get_resource("uid")).startswith(f"{dataset.namespace()}::"),
        "Sample UID has correct namespace",
    )
    tc.assertTrue(
        str(sample.get_resource("label_gt")).startswith(f"{dataset.namespace()}::"),
        "Sample label has correct namespace",
    )
    if deep:
        # Attemt to load input image
        sample.get_resource("input_img_np")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    gp = parser.add_mutually_exclusive_group(required=True)
    gp.add_argument("--name", type=str)
    gp.add_argument("--json", type=str)
    parser.add_argument("--deep", action="store_true")
    args = parser.parse_args()

    if args.name is not None:
        validate({"name": args.name}, args.deep)

    elif args.json is not None:
        import config as pcfg

        configs = [pcfg.config_from_json(args.json, read_from_file=True)]
        config = pcfg.ConfigurationSet(*configs)

        validate(config, args.deep)
