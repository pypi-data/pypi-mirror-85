settings = {
	'name':'Orden trabajo',
    'icon_class':'glyphicon glyphicon-list-alt',
    'url':r'/pedidos/',
    'url_main_path':r'pedidos/',
    'users':[],
}

PERMISSIONS = {
    'Herramientas': {
        'permissions': [
            {
                'name': 'Preferencias',
                'codename': 'preferencias',
            },
            {
                'name': 'Preparar Aplicacion',
                'codename': 'prepararaplicacion',
            },
        ],
    },
    'permissions': [
        {
            'name': 'Agregar Orden de trabajo',
            'codename': 'addordentrabajo',
        },
        {
            'name': 'Editar Orden de trabajo',
            'codename': 'editordentrabajo',
        },
        {
            'name': 'Cambiar progreso',
            'codename': 'progresoorden',
        },
        {
            'name': 'Asignar vendedor',
            'codename': 'asignarvendedor',
        },
        {
            'name': 'Reportes',
            'codename': 'verreportes',
        },
    ],

}