from kedro.pipeline import Pipeline, node

from .nodes import *


def create_pipeline(**kwargs):
    return Pipeline(
        [
            # node(
            #     split_data,
            #     ["twitter_disinfo_raw", "params:example_test_data_ratio"],
            #     dict(
            #         train_x="example_train_x",
            #         train_y="example_train_y",
            #         test_x="example_test_x",
            #         test_y="example_test_y",
            #     ),
            # )
            node(
                remove_rt,
                ["twitter_disinfo_raw"],
                dict(
                    og="original",
                    rt="retweets"
                )
            ),
            node(
                remove_empty,
                ["original"],
                dict(
                    content="content",
                    empty="empty"
                )
            ),
            node(
                language_split,
                ["content"],
                dict(
                    ar_fa="arabic_script",
                    en_tr="latin_script",
                    ru_ot="cyrillic",
                    ja_zh="kanji",
                    ko="korean",
                    other="other"
                )
            ),
            node(
                arabic_split,
                ["arabic_script"],
                dict(
                    ar="arabic",
                    fa="persian",
                    ur="urdu"
                )
            ),
            node(
                latin_split,
                ["latin_script"],
                dict(
                    en="english",
                    tr="turkish"
                )
            )
        ]
    )
