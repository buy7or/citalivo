# citalivo

## Uso

#### Primer Uso

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

En otra terminal

```
ngrok http 5000
```


En [facebook developers](https://developers.facebook.com/apps/1634411890567136/use_cases/customize/wa-settings/?product_route=whatsapp-business&business_id=1244047720790855&use_case_enum=WHATSAPP_BUSINESS_MESSAGING&selected_tab=wa-dev-console)

Añadir webhook la ruta de ngrok con /webhook al final y en el token veify mi_token_personal.

Una vez configurado en el panel de los wbhooks activar el messages.