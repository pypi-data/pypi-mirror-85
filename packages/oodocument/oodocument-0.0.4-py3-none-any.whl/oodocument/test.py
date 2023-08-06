from oodocument import oodocument
data = {}
data['holamundo'] = 'XXX'
oo = oodocument('./input.docx', host='0.0.0.0', port=8001)
oo.replace_with(data, './output.doc', 'doc')
oo.dispose()
