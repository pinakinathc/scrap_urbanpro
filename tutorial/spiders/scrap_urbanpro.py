import scrapy

class UrbanSpider(scrapy.Spider):
	name="urbanpro"

	start_urls =[
		'https://wwww.urbanpro.com/',
	]

	def parse(self, response):
		categories = response.css('div.shdwPart a::attr(href)').extract()
		print "\n\n\nparse running\n\n\n"
		flag=0
		for i, var in enumerate(categories):
			if flag==1:
				yield scrapy.Request(response.urljoin(var), callback=self.parse_city)
			elif (var == unicode('/all-categories')):
				flag=1

	def parse_city(self, response):
		print "\n\n\nparse_city running\n\n\n"
		#the function below will be extract not extract_first in future development
		#we can get a list in order to parse each element in the list of the category 'DELHI'
		#for now we are parsing only tution-classes
		nextpage = response.css('p.popularSubTitle a::attr(href)').extract_first()

		yield scrapy.Request(response.urljoin(nextpage), callback=self.parse_category)

	def parse_category(self, response):
		print "\n\n\nparse_category running\n\n\n"
		#get the list of members
		members = response.css('div.listing-image-box a::attr(href)').extract()

		for member in members:
			yield scrapy.Response(response.urljoin(member), callback=self.parse_member)

	def parse_member(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first().strip()

		yield {
			'image': extract_with_css('div.profileImageHeader img.photo::attr(src)'),
			'name': extract_with_css('div.rightProfileHead h1.profile-name::text'),
			'locality': extract_with_css('span.locality::text'),
			'region': extract_with_css('span.region::text')
			#'postalcode': extract_with_css('span.postal-code::text'),
		}