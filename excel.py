import pandas as pd
import re
file_path = 'random.xlsx'
df = pd.read_excel(file_path)
names_to_filter_OS = ['redhat', 'red hat','Windows']
names_to_filter_language = ['python', 'PYTHON']
def filter_names(cell_value, names_to_filter):
    pattern = re.compile(r'\'(' + '|'.join(re.escape(name) for name in names_to_filter) + r')\s*([^\']*?)\'', flags=re.IGNORECASE)
    matches = pattern.findall(str(cell_value))
    return ', '.join(['\'{} {}\''.format(match[0], match[1].strip()) for match in matches])
df['OS_INFO'] = df.iloc[:, 8].apply(lambda cell_value: filter_names(cell_value, names_to_filter_OS))
df['OS'] = df.iloc[:, 8].apply(lambda cell_value: ', '.join(['Redhat' if 'red hat' in str(cell_value).lower() else '', 'Windows' if 'windows' in str(cell_value).lower() else '']).strip(', '))
df['PROGRAMMING_LANGUAGE'] = df.iloc[:, 8].apply(lambda cell_value: ', '.join(
    lang.capitalize() for lang in [
        'java' if any(lang.lower() in str(cell_value).lower() for lang in ['java', 'jdk', 'java runtime environment', 'jre']) else '',
        'python' if any(lang.lower() in str(cell_value).lower() for lang in ['python']) else '',
        '.NET' if any(lang.lower() in str(cell_value).lower() for lang in ['.net', 'dotnet']) else '',
        'nodejs' if any(lang.lower() in str(cell_value).lower() for lang in ['javascript', 'typescript']) else '',
        'go' if re.search(r'\bgo\b', str(cell_value).lower()) else ''
    ] if lang
))
#df['PYTHON_SPECIFIC'] = df.iloc[:, 8].apply(lambda cell_value: filter_names(cell_value, names_to_filter_language))
df.to_excel('random_filtered.xlsx', index=False)
