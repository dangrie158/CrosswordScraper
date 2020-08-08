import scrapy
import logging

class KreuzwordSpider(scrapy.Spider):
    name = 'crossword'
    start_urls = [
        'https://www.kreuzwortraetsel.de/',
    ]

    def parse(self, response):
        letter_pages = response.css('.a-z-tab-menu ul li a::attr("href")').getall()
        yield from response.follow_all(letter_pages, self.parse_letter_page)

    def parse_letter_page(self, response):
        questions_pages = response.css('.search-result-box .a-z-tab-menu ul li a::attr("href")').getall()
        yield from response.follow_all(questions_pages, self.parse_questions_page)

    def parse_questions_page(self, response):
        questions = response.css('.questions div a::attr("href")').getall()
        yield from response.follow_all(questions, self.parse_question)

    def parse_question(self, response):
        question_texts = response.css('td.puzzle-name a::text').getall()
        solution_texts = response.css('td.solution div.puzzle-solution a::text').getall()
        for question, solution in zip(question_texts, solution_texts):
            yield {
                'q': question.strip(),
                's': solution.strip()
            }