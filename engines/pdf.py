from jinja2 import Environment, FileSystemLoader
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

        env = Environment(autoescape=True, loader=FileSystemLoader('assets/templates'))
        template = env.get_template(template_name)
        return template.render(context)

    def generate_pdf(self) -> bytes:
        """
        Pega a resposta com o documento.
        """

        return HTML(string=self.html_string).write_pdf(presentational_hints=True)
