import json
import os
from typing import Any

from penelope.corpus import CorpusVectorizer, SparvTokenizedCsvCorpus, TokensTransformOpts, VectorizedCorpus
from penelope.corpus.readers import AnnotationOpts
from penelope.utility import getLogger, replace_extension

from .utils import WorkflowException

logger = getLogger("penelope")

# pylint: disable=too-many-arguments


def execute_workflow(
    input_filename: str,
    output_folder: str,
    output_tag: str,
    *,
    filename_field: Any = None,
    filename_pattern: str = '*.*',
    count_threshold: int = None,
    annotation_opts: AnnotationOpts = None,
    tokens_transform_opts: TokensTransformOpts = None,
) -> VectorizedCorpus:

    if not os.path.isfile(input_filename):
        raise WorkflowException(f'no such file: {input_filename}')

    if len(filename_field or []) == 0:
        raise WorkflowException("please specify at least one filename field (e.g. --filename-field='year:_:1')")

    logger.info('Creating new corpus...')

    if VectorizedCorpus.dump_exists(tag=output_tag, folder=output_folder):
        VectorizedCorpus.remove(tag=output_tag, folder=output_folder)

    tokenizer_opts = {
        'filename_pattern': filename_pattern,
        'filename_fields': filename_field,
        'as_binary': False,
    }

    corpus = SparvTokenizedCsvCorpus(
        source=input_filename,
        tokenizer_opts=tokenizer_opts,
        annotation_opts=annotation_opts,
        tokens_transform_opts=tokens_transform_opts,
    )

    logger.info('Creating document-term matrix...')
    vectorizer = CorpusVectorizer()
    v_corpus = vectorizer.fit_transform(corpus)
    # FIXME: #18 count_threshold not used in _vectorize_sparv_csv_corpus.

    logger.info('Saving data matrix...')
    v_corpus.dump(tag=output_tag, folder=output_folder)

    logger.info('Saving parameters JSON...')
    json_filename = os.path.join(output_folder, f"{output_tag}_vectorizer_data.json")
    with open(replace_extension(json_filename, 'json'), 'w') as json_file:
        store_options = {
            'input_filename': input_filename,
            'output_folder': output_folder,
            'output_tag': output_tag,
            'count_threshold': count_threshold,
            'tokenizer_opts': tokenizer_opts,
            'tokens_transform_opts': tokens_transform_opts.props,
            'annotation_opts': annotation_opts.props,
        }
        json.dump(store_options, json_file, indent=4)
    logger.info('Done!')

    return v_corpus
