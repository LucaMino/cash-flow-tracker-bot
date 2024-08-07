import json

def sanitize_response(response_content):
    # json decode
    decoded_content = json.loads(response_content)

    extracted_array = None

    if isinstance(decoded_content, dict):
        # Itera attraverso tutte le chiavi del dizionario
        for key, value in decoded_content.items():
            # Controlla se il valore è una lista
            if isinstance(value, list):
                # Se è una lista, estrai il valore e interrompi il ciclo
                extracted_array = value
                break

    if extracted_array is None:
        extracted_array = decoded_content

    print(extracted_array)

    return extracted_array
