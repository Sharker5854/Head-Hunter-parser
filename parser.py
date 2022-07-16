import csv
import requests
from bs4 import BeautifulSoup
import config



class Parser:
	area = config.HEADHUNTER_AREA_PARAM

	def __init__(self):
		self.profession = input("\nВведите интересующую профессию: ")
		self.pages = int(input("Введите количество страниц для парсинга (на одной странице 50 вакансий): "))


	def get_response(self, page):
		response = requests.get(
			config.URL, headers=config.HEADERS, 
			params={"area" : self.area, "text" : self.profession, "page" : page}
		)
		return response


	def get_page_content(self, response):
		'''Поиск всех данных на одной конкретной page'''
		soup = BeautifulSoup(response.text, "html.parser")
		vacancies = soup.find_all("div", class_="vacancy-serp-item__layout")

		if len(vacancies) == 0:
			return None
		else:
			content = []
			for vac in vacancies:
				title_block = vac.find("a", class_="bloko-link")
				content.append(
					{
						"title" : title_block.get_text(strip=True),
						"link" : title_block.get("href").split("?")[0],
						"salary" : vac.find("span", class_="bloko-header-section-3").get_text().replace("\u202f", "") if ( vac.find("span", class_="bloko-header-section-3") != None ) else "Не указано",
						"company" : vac.find("a", class_="bloko-link bloko-link_kind-tertiary").get_text().replace("\xa0", " ")
					}
				)

			return content


	def write_in_file(self, data):
		try:
			with open(f"C:\\Users\\Admin\\Desktop\\{self.profession.title()}.{config.SAVE_FILE_EXTENSION}", "w", newline="") as file:
				writer = csv.writer(file, delimiter=";")

				writer.writerow(["ДОЛЖНОСТЬ", "ЗАРПЛАТА", "КОМПАНИЯ", "ССЫЛКА НА ВАКАНСИЮ"])
				writer.writerow([""])

				for dataset in data:
					writer.writerow([ dataset["title"], dataset["salary"], dataset["company"], dataset["link"] ])

			print(f"Файл {self.profession.title()}.{config.SAVE_FILE_EXTENSION} сохранён на рабочий стол!")
		except:
			print("Ошибка при записи в файл.")

		input("\n\n-------------------------------\nНажмите Enter чтобы завершить.")


	def parse(self):
		print("\nПоиск вакансий в Москве...\n")
		responses = []
		for page in range(self.pages):
			responses.append(self.get_response(page))

		data = []
		if self.get_page_content(responses[0]) == None:
			print("По вашему запросу ничего не найдено!")
		else:
			for resp in responses:
				content = self.get_page_content(resp)
				if content != None:
					for dataset in content:
						data.append(dataset)
				else:
					break

		self.write_in_file(data)



Parser().parse()	