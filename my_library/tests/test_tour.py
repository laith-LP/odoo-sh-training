# -*- coding: utf-8 -*-
from odoo.tests.common import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestBookUI(HttpCase):

    def test_01_book_tour(self):
        """Books UI tour test case"""
        self.browser_js("/web",
                        'odoo.__DEBUG__.services["web_tour.tour"].run("library_tour")',
                        "odoo.__DEBUG__.services['web_tour.tour'].tours.library_tour.ready",
                        login="admin")
