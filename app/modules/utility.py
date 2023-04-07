def generate_dropdown_html(option_list: list, button_title: str, curr_href: str = None) -> str:

    html = ''
    html += '<div class="dropdown">'
    html += """<button class="btn btn-secondary dropdown-toggle"
                type="button" id="dropdownMenuButton"
                data-toggle="dropdown" aria-haspopup="true"
                aria-expanded="false">"""

    html += f'{button_title}'

    html += '</button>'
    html += '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
    for option in option_list:

        if curr_href is None:
            html += f'<a class="dropdown-item" href="{option}">{option}</a>'
        else:
            html += f'<a class="dropdown-item" href="{curr_href}?district={option}">{option}</a>'

    html += '</div>'
    html += '</div>'

    return html
