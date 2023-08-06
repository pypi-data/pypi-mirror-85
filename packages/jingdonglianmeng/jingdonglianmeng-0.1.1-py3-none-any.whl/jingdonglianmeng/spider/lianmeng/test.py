import json
import requests

start_url = "https://item-soa.jd.com/getWareBusiness?skuId=5964534"
headers = {
    'cookie': 'thor=90CEC7A0E588FF207139503BF0056761801C5F1B4029EFE863207F36444BEC6D4AF0C3DE6065B8846CDE86BBDBD77B4A9A6B5D3FBA2204DB0A541E66DC7B2EC7233251ECFE39EC52B67AC353334B71F943DB62635CECB52605BF6F729F4B73156666FE74B6DF4CC390FF35B5BACEB38A25BB2CF1E5468E95E783FB0EFFD8196875BBE5C21ACF6FD4E21D1ED0D50465C6F7B826A074077667AFE0E4DF6BA91B24; pin=jd_4517f39da4099',
    'accept-encoding': 'gzip,deflate,br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'upgrade-insecure-requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
}

res = requests.get(start_url, headers=headers)
print(json.dumps(res.json(), indent=2, ensure_ascii=False))
