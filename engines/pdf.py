from jinja2 import Environment, FileSystemLoader
from fastapi.responses import Response
from weasyprint import HTML


class GeneratePDF:
    """
    Classe Resposável por gerar o PDF.
    """

    def __init__(self, template: str, context: dict, filename: str) -> None:
        """
        Construtor
        """

        self.html_string = self.render_to_string(template, context)
        self.filename = filename

    def render_to_string(self, template_name: str, context: dict) -> str:
        """
        Render html to string
        """

        env = Environment(autoescape=True, loader=FileSystemLoader('templates'))
        template = env.get_template(template_name)
        return template.render(context)

    def get_response(self) -> Response:
        """
        Pega a resposta com o documento.
        """

        pdf = HTML(string=self.html_string).write_pdf(presentational_hints=True)

        response = Response(
            content=pdf,
            media_type='application/pdf',
            headers={"Content-Disposition": f"inline; filename={self.filename}.pdf"}
        )

        return response
