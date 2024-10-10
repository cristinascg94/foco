from django.contrib import admin
from .models import  Corto, Pase, UsuarioAleatorio, Votacion
from docx import Document
import io
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from django.http import HttpResponse



def set_cell_border(cell, **kwargs):
    """
    Función para establecer bordes en las celdas.
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    
    # Los bordes posibles son 'top', 'left', 'bottom', 'right', 'insideH', 'insideV'
    for edge in ('top', 'left', 'bottom', 'right'):
        edge_elem = OxmlElement(f'w:{edge}')
        edge_elem.set(qn('w:val'), 'single')
        edge_elem.set(qn('w:sz'), '8')  # Tamaño del borde (puedes ajustarlo)
        edge_elem.set(qn('w:space'), '0')
        edge_elem.set(qn('w:color'), '000000')  # Color del borde en hexadecimal
        tcPr.append(edge_elem)

def generar_word(modeladmin, request, queryset):
    # Filtrar los usuarios
    for obj in queryset:
        print(obj.pase)
        pase = Pase.objects.get(pase=obj.pase)
        usuarios_filtrados = UsuarioAleatorio.objects.filter(pase=pase)

        # Crear el documento Word
        doc = Document()
        doc.add_heading(f'Usuarios con Pase: {pase}', 0)

        # Agregar tabla con dos columnas
        table = doc.add_table(rows=1, cols=2)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Nombre'
        hdr_cells[1].text = 'Pase'

        # Aplicar bordes a la fila de encabezado
        for cell in hdr_cells:
            set_cell_border(cell)

        # Rellenar la tabla con los usuarios filtrados y aplicar bordes
        for usuario in usuarios_filtrados:
            row_cells = table.add_row().cells
            row_cells[0].text = f"{usuario} {pase}"
            # Aplicar bordes a cada celda
            for cell in row_cells:
                set_cell_border(cell)

        # Preparar la respuesta HTTP
        f = io.BytesIO()
        doc.save(f)
        f.seek(0)

        response = HttpResponse(f.getvalue(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=usuarios_con_pase_{pase}.docx'

    return response

generar_word.short_description = "generar_word"


admin.site.register(Corto)

admin.site.register(UsuarioAleatorio)

class PaseAdmin(admin.ModelAdmin):
    actions = [generar_word]
    list_display = ('pase',)

admin.site.register(Pase, PaseAdmin)


class VotacionAdmin(admin.ModelAdmin):
    # Muestra las columnas 'corto', 'usuario' y 'votacion' en la lista del admin
    list_display = ('corto', 'usuario', 'votacion')
admin.site.register(Votacion, VotacionAdmin)