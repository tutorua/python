# https://dou.ua/forums/topic/49699/?from=comment-digest_bc&utm_source=digest-comments&utm_medium=email&utm_campaign=26072024#2858792

# read PDF
def extract_pdf_text(pdf_bytes: bytes) -> str:
    pdf_text = ''
    pdf_document = fitz.open(PDF_EXT, pdf_bytes)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text_page = page.get_textpage()
        pdf_text += text_page.extractText()

    return pdf_text

# extract the fields names  
def extract_pdf_fields(pdf_bytes: bytes) -> list[dict]:
    form_fields = []
    pdf_document = fitz.open(PDF_EXT, pdf_bytes)

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        widget_list = page.widgets()
        if widget_list:
            for widget in widget_list:
                form_fields.append({
                    'name': widget.field_name,
                    'label': widget.field_label,
                    'type': widget.field_type_string,
                    'max_length': widget.text_maxlen
                })

    return form_fields


# call AI to fill in the form fields ( OpenAI та модель GPT-4o )
def fill_fields_prompt(pdf_text: str, fields: list[dict], source_info: str) -> str:
    return f"""
        You are an automated PDF forms filler.
        Your job is to fill the following form fields using the provided materials.
        Field keys will tell you which values they expect:
        {json.dumps(fields)}

        Materials:
        - Text extracted from the PDF form, delimited by <>:
        <{pdf_text}>

        - Source info attached by user, delimited by ##:
        #{source_info}#
        
        Output a JSON object with key-value pairs where:
        - key is the 'name' of the field,
        - value is the field value you assigned to it.
    """
    
 
#  create a dictionary (field: value) to be used for the filling the form
def call_openai(prompt: str, gpt_model: str = 'gpt-4o'):
    response =  openai_client.chat.completions.create(
        model=gpt_model,
        messages=[{'role': 'system', 'content': prompt}],
        response_format={"type": "json_object"},
        timeout=TIMEOUT,
        temperature=0
    )
    
    response_data = response.choices[0].message.content.strip()
    return json.loads(response_data)
    
    
# fill in PDF form
def fill_pdf_fields(pdf_bytes: bytes, field_values: dict) -> io.BytesIO:
    pdf_document = fitz.open(PDF_EXT, pdf_bytes)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        widget_list = page.widgets()

        if widget_list:
            for widget in widget_list:
                field_name = widget.field_name
                if field_name in field_values:
                    widget.field_value = field_values[field_name]
                    widget.update()
                    
    output_stream = io.BytesIO()
    pdf_document.save(output_stream)
    output_stream.seek(0)

    return output_stream
    


