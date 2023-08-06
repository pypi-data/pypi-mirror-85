from typing import Sequence, List, Optional, Union
import importlib.util
import os
import sys

from pyexlatex.logic.output.api.formats import OutputFormats
from pyexlatex.models.document import DocumentBase

sys.path.append(os.path.abspath(os.getcwd()))  # needed to be able to import local plbuild directory

IGNORED_FILES = [
    '__init__.py',
]


def get_all_source_files() -> List[str]:
    from plbuild.paths import (
        SLIDES_SOURCE_PATH,
        slides_source_path,
        DOCUMENTS_SOURCE_PATH,
        documents_source_path,
    )
    slide_sources = [file for file in next(os.walk(SLIDES_SOURCE_PATH))[2] if file not in IGNORED_FILES]
    slide_sources = [slides_source_path(file) for file in slide_sources]
    doc_sources = [file for file in next(os.walk(DOCUMENTS_SOURCE_PATH))[2] if file not in IGNORED_FILES]
    doc_sources = [documents_source_path(file) for file in doc_sources]
    return slide_sources + doc_sources


def create_presentation_template(name: str):
    from plbuild.paths import (
        slides_source_path,
    )
    base_file_name = get_file_name_from_display_name(name)
    full_file_name = f'{base_file_name}.py'
    file_path = slides_source_path(full_file_name)
    create_template(
        [
            'general_imports',
            'presentation_imports',
            'author',
            'presentation',
            'general',
        ],
        out_path=file_path
    )


def create_document_template(name: str):
    from plbuild.paths import (
        documents_source_path,
    )
    base_file_name = get_file_name_from_display_name(name)
    full_file_name = f'{base_file_name}.py'
    file_path = documents_source_path(full_file_name)
    create_template(
        [
            'general_imports',
            'document_imports',
            'author',
            'document',
            'general',
        ],
        out_path=file_path
    )


def create_template(template_names: Sequence[str], out_path: str):
    from plbuild.paths import (
        templates_path_func
    )
    template_paths = [templates_path_func(template + '.py') for template in template_names]
    template_str = _create_template_str(template_paths)
    with open(out_path, 'w') as f:
        f.write(template_str)


def _create_template_str(template_paths: Sequence[str]) -> str:
    template_str = ''
    for path in template_paths:
        with open(path, 'r') as f:
            template_str += f.read()
    template_str += '\n'
    return template_str



def get_file_name_from_display_name(name: str) -> str:
    """
    Converts name to snake case and lower case for use in file name

    :param name: display name, can have spaces and capitalization
    :return:
    """
    return name.replace(' ', '_').lower()


def build_all(desired_output_format: Optional[OutputFormats] = None):
    files = get_all_source_files()
    [build_by_file_path(file, desired_output_format=desired_output_format) for file in files]


def build_by_file_path(file_path: str, desired_output_format: Optional[OutputFormats] = None):
    _print_now(f'Building {file_path}')
    mod = _module_from_file(file_path)

    optional_attrs = dict(
        title='TITLE',
        short_title='SHORT_TITLE',
        subtitle='SUBTITLE',
        handouts_outfolder='HANDOUTS_OUTPUT_LOCATION',
        index='ORDER',
        authors='AUTHORS',
        short_author='SHORT_AUTHOR',
        institutions='INSTITUTIONS',
        short_institution='SHORT_INSTITUTION',
        output_name='OUTPUT_NAME',
        default_output_format='DEFAULT_OUTPUT_FORMAT',
    )

    kwargs = dict(
        pl_class=mod.DOCUMENT_CLASS,
        outfolder=mod.OUTPUT_LOCATION,
    )

    for kwarg, mod_attr in optional_attrs.items():
        value = getattr(mod, mod_attr, None)
        if value is not None:
            kwargs.update({kwarg: value})

    passed_kwargs = getattr(mod, 'DOCUMENT_CLASS_KWARGS', None)
    if passed_kwargs:
        kwargs.update(passed_kwargs)

    output_format = OutputFormats.PDF
    if 'default_output_format' in kwargs:
        output_format = kwargs.pop('default_output_format')
    if desired_output_format is not None:
        output_format = desired_output_format

    build_from_content(
        mod.get_content(),
        output_format=output_format,
        **kwargs
    )
    out_name = _get_out_name(**kwargs)
    _print_now(f'Done creating {mod.DOCUMENT_CLASS.__name__}: {out_name}.')


def build_from_content(content, pl_class, outfolder: str,
                       handouts_outfolder: Optional[str] = None,
                       index: Optional[int] = None,
                       output_format: OutputFormats = OutputFormats.PDF, **kwargs):
    out_name = _get_out_name(index=index, **kwargs)
    if 'output_name' in kwargs:
        kwargs.pop('output_name')

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    fmp = pl_class(
        content,
        **kwargs
    )
    _output_document(fmp, outfolder, out_name, output_format=output_format)
    if handouts_outfolder is not None:
        fmp_handout = pl_class(
            content,
            handouts=True,
            **kwargs
        )
        _output_document(fmp_handout, handouts_outfolder, out_name, output_format=output_format)


def _output_document(doc: DocumentBase, outfolder: str, out_name: str,
                     output_format: OutputFormats = OutputFormats.PDF):
    if output_format == OutputFormats.PDF:
        out_method = getattr(doc, 'to_pdf')
    elif output_format == OutputFormats.HTML:
        out_method = getattr(doc, 'to_html')
    else:
        raise ValueError(f'unsupported output format {output_format}')

    out_method(outfolder, out_name)


def _get_out_name(index: Optional[int] = None, output_name: Optional[str] = None,
                  **kwargs: dict) ->  str:
    if output_name is None:
        output_name = 'untitled'

    if index is None:
        return output_name

    return f'{index} {output_name}'


def _module_from_file(file_path: str):
    mod_name = os.path.basename(file_path).strip('.py')
    return _module_from_file_and_name(file_path, mod_name)


def _module_from_file_and_name(file_path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _print_now(*args):
    print(*args)
    sys.stdout.flush()

if __name__ == '__main__':
    build_all()