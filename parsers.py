import csv
import requests
from requests import Response
from bs4 import BeautifulSoup
import config


class Parser:
	def __init__(self, profession, pages=3):
		self.profession = profession
		self.pages = pages
		self.area_param_name = config.SITES[self.site]["area_param_name"]
		self.profession_param_name = config.SITES[self.site]["profession_param_name"]
		self.page_param_name = config.SITES[self.site]["page_param_name"]

	def get_response(self, page) -> Response:
		response = requests.get(
			config.SITES[self.site]["url"], headers=config.HEADERS,
			params={self.area_param_name: self.area, self.profession_param_name: self.profession, self.page_param_name: page},
		)
		return response

	def get_page_content(self, response: Response):
		"Вытащить все нужные элементы из полученного HTML-ответа"
		raise NotImplementedError()


class HeadHunter(Parser):
	area = config.HEADHUNTER_AREA_PARAM
	site = "HeadHunter"

	def get_page_content(self, response: Response):
		'''Поиск всех данных на одной конкретной page'''
		soup = BeautifulSoup(response.text, "html.parser")
		vacancies = soup.find_all("div", class_="vacancy-serp-item__layout")
		if len(vacancies) == 0:
			return None
		else:
			content = []
			for vac in vacancies:
				title_block = vac.find("a", class_="serp-item__title")
				content.append(
					{
						"title" : title_block.get_text(strip=True),
						"link" : title_block.get("href").split("?")[0],
						"salary" : vac.find("span", class_="bloko-header-section-3").get_text().replace("\u202f", "") if ( vac.find("span", class_="bloko-header-section-3") != None ) else "Не указано",
						"company" : vac.find("a", class_="bloko-link bloko-link_kind-tertiary").get_text().replace("\xa0", " ") if ( vac.find("a", class_="bloko-link bloko-link_kind-tertiary") != None ) else "Компания не указана",
					}
				)
			return content

	def parse(self):
		print(f"\nПоиск вакансий в Москве на {self.site}...\n")
		responses = []
		for page in range(1, self.pages+1):
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
		return data


class SuperJob(Parser):
	site = "SuperJob"
	area = config.SUPERJOB_AREA_PARAM

	def get_page_content(self, response: Response):
		'''Поиск всех данных на одной конкретной page'''
		soup = BeautifulSoup(response.text, "html.parser")
		vacancies = soup.find_all("div", class_="f-test-vacancy-item")
		if len(vacancies) == 0:
			return None
		else:
			content = []
			for vac in vacancies:
				title_block = vac.find("a", class_="YrERR")
				salary_block = vac.find("div", class_="f-test-text-company-item-salary")
				content.append(
					{
						"title" : title_block.get_text(strip=True),
						"link" : config.SITES[self.site]["host"] + title_block.get("href"),
						"salary" : salary_block.find("span").get_text().replace("&nbsp;", " ").replace("\u20bd", "руб") if ( salary_block.find("span").get_text().replace("&nbsp;", " ").replace("\u20bd", "руб") != None ) else "Не указано",
						"company" : vac.find("a", class_="_198Ox").get_text() if ( vac.find("a", class_="_198Ox") != None ) else "Компания не указана",
					}
				)
			return content

	def parse(self):
		print(f"\nПоиск вакансий в Москве на {self.site}...\n")
		responses = []
		for page in range(1, self.pages+1):
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
		return data


class RabotaRu(Parser):
	site = "RabotaRu"
	area = config.RABOTARU_SORT_PARAM

	def get_page_content(self, response: Response):
		'''Поиск всех данных на одной конкретной page'''
		soup = BeautifulSoup(response.text, "html.parser")
		vacancies = soup.find_all("div", class_="vacancy-preview-card__wrapper")
		if len(vacancies) == 0:
			return None
		else:
			content = []
			for vac in vacancies:
				title_block = vac.find("a", class_="vacancy-preview-card__title_border")
				salary_block = vac.find("div", class_="vacancy-preview-card__salary")
				try:
					company = vac.find("span", class_="vacancy-preview-card__company-name").find("a").get_text(strip=True)
				except AttributeError:
					company = "Не указано"
				content.append({
					"title" : title_block.get_text(strip=True),
					"link" : config.SITES[self.site]["host"] + title_block.get("href"),
					"salary" : salary_block.find("a").get_text().replace("&nbsp;", "") if ( salary_block.find("a").get_text() != None ) else "Не указано",
					"company" : company
				})
			return content

	def parse(self):
		print(f"\nПоиск вакансий в Москве на {self.site}...\n")
		responses = []
		for page in range(1, self.pages+1):
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
		return data


def write_in_file(profession, dataset):
	try:
		with open(f"C:\\Users\\Admin\\Desktop\\{profession.title()}.{config.SAVE_FILE_EXTENSION}", "w", newline="") as file:
			writer = csv.writer(file, delimiter=";")
			for data in dataset:
				writer.writerow([data[0]])
				writer.writerow([""])
				writer.writerow(["ДОЛЖНОСТЬ", "ЗАРПЛАТА", "КОМПАНИЯ", "ССЫЛКА НА ВАКАНСИЮ"])
				writer.writerow([""])
				for dataset in data[1]:
					writer.writerow([ dataset["title"], dataset["salary"], dataset["company"], dataset["link"] ])
				writer.writerow([""])
				writer.writerow([""])
				writer.writerow([""])
		print(f"Файл {profession.title()}.{config.SAVE_FILE_EXTENSION} сохранён на рабочий стол!")
	except:
		print("Ошибка при записи в файл.")
	input("\n\n-------------------------------\nНажмите Enter чтобы завершить.")


def main():
	profession = input("\nВведите интересующую профессию: ")
	pages = int(input("Введите количество страниц для парсинга на каждом сайте: "))
	site_results = [
		(HeadHunter.site, HeadHunter(profession, pages).parse() ),
		(SuperJob.site, SuperJob(profession, pages).parse() ),
		(RabotaRu.site, RabotaRu(profession, pages).parse() )
	]
	write_in_file(profession, site_results)
	
	

if __name__ == "__main__":
	main()