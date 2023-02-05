SITES = {
	"HeadHunter": {
		"host" : "https://hh.ru",
		"url" : "https://hh.ru/search/vacancy/",
		"area_param_name" : "area",
		"profession_param_name" : "text",
		"page_param_name" : "page"
	},
	"SuperJob": {
		"host" : "https://www.superjob.ru",
		"url" : "https://www.superjob.ru/vakansii/",
		"area_param_name" : "geo[t][0]",
		"profession_param_name" : "keywords",
		"page_param_name" : "page"
	},
	"RabotaRu": {
		"host" : "https://www.rabota.ru",
		"url" : "https://www.rabota.ru/vacancy/",
		"area_param_name" : "sort",
		"profession_param_name" : "query",
		"page_param_name" : "page"
	},
	"JobLab": {
		"host" : "https://joblab.ru",
		"url" : ""
	}
}

HEADHUNTER_AREA_PARAM = 1  # номер обозначает город, в котором ищем работу (1 - Москва, 2 - Питер и т.д.)
SUPERJOB_AREA_PARAM = 4  # 4 - Москва
RABOTARU_SORT_PARAM = "relevance"  # автоматически ищется в Москве, но есть другой параметр сортировки

HEADERS = {
	"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.0.1842 Yowser/2.5 Safari/537.36"
}

SAVE_FILE_EXTENSION = "csv"