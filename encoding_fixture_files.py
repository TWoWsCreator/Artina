import codecs

list_of_path_fixtures = ['paintings/fixtures/painting_fixture.json',
                         'artists/fixtures/artists_fixture.json',
                         'galleries/fixtures/galleries_fixture.json']
# with open('a.txt', 'r', encoding='utf-8') as file:
#     enc = file.encode('ascii')
# for path in list_of_path_fixtures:
#     encoded = codecs.open(path, 'r', 'utf-8').read().encode(
#         'ascii', 'backslashreplace')
#     open(path, 'w').write(encoded)


encoded = codecs.open('a.txt', 'r', 'cp1252').read()
print(encoded)