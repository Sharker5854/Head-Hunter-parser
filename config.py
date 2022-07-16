HOST = "https://hh.ru/"
URL = "https://hh.ru/search/vacancy/"

HEADHUNTER_AREA_PARAM = 1  # номер обозначает город, в котором ищем работу (1 - Москва, 2 - Питер и т.д.)

HEADERS = {
	"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.0.1842 Yowser/2.5 Safari/537.36"
}

SAVE_FILE_EXTENSION = "csv"