from haversine import haversine
import json
import jsonify
import requests
import re
import pathlib
# {"a":"b", "b":[c, d]}
mbti = "{'hotples': '[HotpleVO(htId=155, busnNum=null, goId=ChIJy4KJO6HhZTURgJPKSYiFpzg, busnName=우야지막창 복현점, " \
       "htAddr=북구 복현1동 402-10, htAddrDet=null, htZip=null, htCont=null, goGrd=3.8, htTel=null, htImg=null, " \
       "uploadPath=null, fileName=null, htLat=35.8964074, htLng=128.6145282, uCode=null, category=7, ttKind=null)," \
       "HotpleVO(htId=156, busnNum=null, goId=ChIJj4_mr-zhZTURziGhhSHoIZ4, busnName=막창도둑 복현점, htAddr=북구 복현1동 경진로1길 " \
       "11, htAddrDet=null, htZip=null, htCont=null, goGrd=3.9, htTel=null, htImg=null, uploadPath=null, " \
       "fileName=null, htLat=35.8964673, htLng=128.6147131, uCode=null, category=7, ttKind=null),HotpleVO(htId=157, " \
       "busnNum=null, goId=ChIJWakT-6PhZTURZM6UYXxZWgc, busnName=대구생막창, htAddr=북구 복현1동 426-1, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=3.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8959663, " \
       "htLng=128.6166937, uCode=null, category=7, ttKind=null),HotpleVO(htId=172, busnNum=null, " \
       "goId=ChIJfU_xpQrhZTURlpUzSXK5MT0, busnName=박준오선산곱창, htAddr=산격동 1308-10번지 1층 북구 대구광역시 KR, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=2.5, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8946985, " \
       "htLng=128.6106403, uCode=null, category=7, ttKind=null),HotpleVO(htId=291, busnNum=null, " \
       "goId=ChIJPwdCS6HhZTURDwAbPMIU0JM, busnName=다함께야구왕 복현오거리점, htAddr=북구 복현동 동북로 212, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=3.3, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8990668, " \
       "htLng=128.6076915, uCode=null, category=24, ttKind=null),HotpleVO(htId=309, busnNum=null, " \
       "goId=ChIJQ0J_XqXhZTURADF1QOAdDUs, busnName=스카이스포츠, htAddr=북구 복현2동 190-1, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=5.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8994193, " \
       "htLng=128.6203551, uCode=null, category=24, ttKind=null),HotpleVO(htId=79, busnNum=null, " \
       "goId=ChIJEfo31qfhZTURi78JnHKlNjQ, busnName=투존치킨, htAddr=산격동 478-13번지 북구 대구광역시 KR, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=5.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.902352, " \
       "htLng=128.6131972, uCode=null, category=7, ttKind=null),HotpleVO(htId=83, busnNum=null, " \
       "goId=ChIJGxkN-bXhZTURVGkxKE0LNqw, busnName=보쌈족발, htAddr=불로동 959번지 2층 동구 대구광역시 KR, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=3.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.9004288, " \
       "htLng=128.6317686, uCode=null, category=7, ttKind=null),HotpleVO(htId=119, busnNum=null, " \
       "goId=ChIJayX_KKPhZTUR_Xsybj3G_Gg, busnName=꼬부리24시전주콩나물국밥ㆍ보쌈 복현직영점, htAddr=북구 복현1동 479-2, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=4.3, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8926399, " \
       "htLng=128.6210089, uCode=null, category=7, ttKind=null),HotpleVO(htId=360, busnNum=null, " \
       "goId=ChIJhRnFJKHhZTUR24GN8yKQORQ, busnName=스페셜당구클럽, htAddr=북구 복현동 402-1번지 5층, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8966052, " \
       "htLng=128.6142561, uCode=null, category=24, ttKind=null),HotpleVO(htId=377, busnNum=null, " \
       "goId=ChIJEfAH56LhZTURuqf0BdJh7-U, busnName=복현종합시장, htAddr=북구 복현동 462, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=3.1, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8924059, " \
       "htLng=128.6200812, uCode=null, category=52, ttKind=null),HotpleVO(htId=425, busnNum=null, " \
       "goId=ChIJbTDHtLvhZTURbhl9zwsCgJ4, busnName=뉴욕피자, htAddr=복현동 245-15번지 1층 북구 대구광역시 KR, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=4.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.895487, " \
       "htLng=128.6252138, uCode=null, category=4, ttKind=null),HotpleVO(htId=621, busnNum=null, " \
       "goId=ChIJ61qWjwThZTURCoixw1CX74o, busnName=우리동네 통삼겹숯불갈비, htAddr=북구 복현1동 동북로 212 1층, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=4.9, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8971072, " \
       "htLng=128.6152968, uCode=null, category=1, ttKind=null),HotpleVO(htId=622, busnNum=null, " \
       "goId=ChIJNb_h7cHhZTURYcvyufLz2mk, busnName=정민네 (한식, 밥집), htAddr=북구 복현1동 428-2, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=5.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8946516, " \
       "htLng=128.6178588, uCode=null, category=1, ttKind=null),HotpleVO(htId=636, busnNum=null, " \
       "goId=ChIJHafn92DhZTURKiiYXv4fFn0, busnName=다담뜰한식뷔페 엑스코점, htAddr=북구 신관 엑스코로 10 2층, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.2, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.907821, " \
       "htLng=128.612776, uCode=null, category=1, ttKind=null),HotpleVO(htId=675, busnNum=null, " \
       "goId=ChIJneCIJ73hZTUR65ml9FBBSRc, busnName=빵굽는사람들, htAddr=신암동 645-4번지 하나로마트 내 동구 대구광역시 KR, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=4.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8919888, " \
       "htLng=128.6222876, uCode=null, category=12, ttKind=null),HotpleVO(htId=676, busnNum=null, " \
       "goId=ChIJd1HALrzhZTUR-qxDzWTmTtg, busnName=파네토네 베이커리, htAddr=북구 복현동 복현푸르지오아파트 상가 119호, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=4.1, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.890827, " \
       "htLng=128.6263623, uCode=null, category=12, ttKind=null),HotpleVO(htId=691, busnNum=null, " \
       "goId=ChIJU9A6wLDhZTURQfbrInG6xe4, busnName=퍼즈X멜트베이커리, htAddr=북구 복현2동 270-1, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=3.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8990195, " \
       "htLng=128.6254953, uCode=null, category=12, ttKind=null),HotpleVO(htId=483, busnNum=null, " \
       "goId=ChIJXUmO4K7hZTURtY_Quhev0Gk, busnName=천안문, htAddr=북구 복현2동 검단로 64, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=2.9, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.9033748, " \
       "htLng=128.6172774, uCode=null, category=5, ttKind=null),HotpleVO(htId=491, busnNum=null, " \
       "goId=ChIJh39VFXXhZTURWYWrYFmFqGw, busnName=타이짬뽕, htAddr=북구 산격3동 1333, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=3.3, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8932895, " \
       "htLng=128.6097046, uCode=null, category=5, ttKind=null),HotpleVO(htId=546, busnNum=null, " \
       "goId=ChIJ0coovabhZTUR02V0O9-2UtA, busnName=롯데리아 대구복현점, htAddr=북구 복현2동 539-123, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=3.6, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8981551, " \
       "htLng=128.6154426, uCode=null, category=6, ttKind=null),HotpleVO(htId=843, busnNum=null, " \
       "goId=ChIJgQU4EXXhZTUR9qYlBKjlqIA, busnName=핸즈커피 경대점, htAddr=북구 산격3동 1327-17, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=3.9, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8932945, " \
       "htLng=128.6090822, uCode=null, category=13, ttKind=null),HotpleVO(htId=870, busnNum=null, " \
       "goId=ChIJJzEAh0LhZTUROEgV2mVxxzU, busnName=월드21게임랜드, htAddr=북구 산격3동 1337-1, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=5.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8927878, " \
       "htLng=128.6090553, uCode=null, category=20, ttKind=null),HotpleVO(htId=888, busnNum=null, " \
       "goId=ChIJVUpG-qXhZTUR4bFW3651AIc, busnName=엔젤PC방, htAddr=복현동 539-113번지 상가 108동 지하층 층 101호 복현청구타운 북구 대구광역시 KR, " \
       "htAddrDet=null, htZip=null, htCont=null, goGrd=2.0, htTel=null, htImg=null, uploadPath=null, fileName=null, " \
       "htLat=35.9006787, htLng=128.6168111, uCode=null, category=20, ttKind=null),HotpleVO(htId=1048, busnNum=null, " \
       "goId=ChIJ-WzzcpzhZTURyhCA1cZnFaA, busnName=꽉찬맥주, htAddr=KR 대구광역시 동구 신암동 1833번지 304동 동1층 103호 이안동대구, " \
       "htAddrDet=null, htZip=null, htCont=null, goGrd=2.0, htTel=null, htImg=null, uploadPath=null, fileName=null, " \
       "htLat=35.8862426, htLng=128.6157057, uCode=null, category=30, ttKind=null),HotpleVO(htId=1131, busnNum=null, " \
       "goId=ChIJba_m86DhZTURX9xa4Bt4MpU, busnName=꿈에포차, htAddr=산격동 1279-6번지 1층 북구 대구광역시 KR, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=3.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8960078, " \
       "htLng=128.6126431, uCode=null, category=31, ttKind=null),HotpleVO(htId=1189, busnNum=null, " \
       "goId=ChIJlZP186bhZTURwtRas_sc7I4, busnName=정막걸리, htAddr=북구 산격동 495-14번지, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8992348, " \
       "htLng=128.6147007, uCode=null, category=32, ttKind=null),HotpleVO(htId=1191, busnNum=null, " \
       "goId=ChIJkwKe6KPhZTURJN59BnOSf0s, busnName=신바람야시장, htAddr=북구 복현1동 425-7, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.1, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8953991, " \
       "htLng=128.6169286, uCode=null, category=32, ttKind=null),HotpleVO(htId=1098, busnNum=null, " \
       "goId=ChIJQ5Vc66PhZTURwGFNiVgRejE, busnName=2060식당, htAddr=북구 복현1동 426-7, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=3.9, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8951749, " \
       "htLng=128.6176513, uCode=null, category=31, ttKind=null),HotpleVO(htId=1103, busnNum=null, " \
       "goId=ChIJUUHt-q_hZTURGos4J3EgtNs, busnName=킹스비어, htAddr=복현동 89-16번지 1층 북구 대구광역시 KR, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=3.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.899957, " \
       "htLng=128.6209486, uCode=null, category=31, ttKind=null),HotpleVO(htId=896, busnNum=null, " \
       "goId=ChIJeQI59BDhZTURnenq0ciaH9o, busnName=볼륨업피씨방, htAddr=북구 산격동 1341-2, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.5, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8927321, " \
       "htLng=128.6092491, uCode=null, category=20, ttKind=null),HotpleVO(htId=907, busnNum=null, " \
       "goId=ChIJ6TfAQnThZTUR6NNsgcwGOVQ, busnName=포그네PC방, htAddr=산격동 1414-1번지 2층 북구 대구광역시 KR, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=3.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8924357, " \
       "htLng=128.6071814, uCode=null, category=20, ttKind=null),HotpleVO(htId=984, busnNum=null, " \
       "goId=ChIJ0yF52cHhZTURMWLjYFyuww8, busnName=아지트동전노래방, htAddr=북구 복현동 364-4, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.8, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8923141, " \
       "htLng=128.6228355, uCode=null, category=23, ttKind=null),HotpleVO(htId=986, busnNum=null, " \
       "goId=ChIJEwZCEHXhZTURVdKXwkLYQTE, busnName=백악관노래방, htAddr=북구 산격동 대학로23길 35, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8930152, " \
       "htLng=128.609142, uCode=null, category=23, ttKind=null),HotpleVO(htId=988, busnNum=null, " \
       "goId=ChIJqW8ARqHhZTURrBlRPWVgN30, busnName=시크릿노래방, htAddr=복현동 413-6번지 3층 북구 대구광역시 KR, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=4.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8963954, " \
       "htLng=128.6152858, uCode=null, category=23, ttKind=null),HotpleVO(htId=991, busnNum=null, " \
       "goId=ChIJx9bvnc7hZTURa4yjQrt4SD4, busnName=가락궁노래방, htAddr=지저동 668-11번지 지하동 1층 성원빌딩 동구 대구광역시 KR, " \
       "htAddrDet=null, htZip=null, htCont=null, goGrd=2.0, htTel=null, htImg=null, uploadPath=null, fileName=null, " \
       "htLat=35.8972615, htLng=128.6389415, uCode=null, category=23, ttKind=null),HotpleVO(htId=1346, busnNum=null, " \
       "goId=ChIJ3weopavhZTUR_OKGfAdIhyU, busnName=(주)아이엠전시문화, htAddr=북구 산격2동 1705-3, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.9086261, " \
       "htLng=128.6142757, uCode=null, category=41, ttKind=null),HotpleVO(htId=1347, busnNum=null, " \
       "goId=ChIJR3W9DHXhZTURd3LFbikS2a8, busnName=경북대학교 미술관, htAddr=북구 산격동 대학로 80, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.1, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8925724, " \
       "htLng=128.6098044, uCode=null, category=41, ttKind=null),HotpleVO(htId=1348, busnNum=null, " \
       "goId=ChIJfTjGJQfhZTURCyG2gxTmO0o, busnName=원갤러리, htAddr=산격동 1618번지 북구 대구광역시 KR, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.9080526, " \
       "htLng=128.6087996, uCode=null, category=41, ttKind=null),HotpleVO(htId=1353, busnNum=null, " \
       "goId=ChIJCWV2KarhZTURWQmnl51dwfw, busnName=채움갤러리, htAddr=산격동 1676번지 지하동 2층 대구전시컨벤션센터 북구 대구광역시 KR, " \
       "htAddrDet=null, htZip=null, htCont=null, goGrd=5.0, htTel=null, htImg=null, uploadPath=null, fileName=null, " \
       "htLat=35.9071971, htLng=128.6132633, uCode=null, category=41, ttKind=null),HotpleVO(htId=1357, busnNum=null, " \
       "goId=ChIJX5BVVb3hZTURNsErZS0l0oc, busnName=대구광역시립동부도서관, htAddr=동구 신암동 신암북로11길 54, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.5, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8901537, " \
       "htLng=128.6216009, uCode=null, category=42, ttKind=null),HotpleVO(htId=1359, busnNum=null, " \
       "goId=ChIJ04CGVqnhZTURMF5nbz91iHw, busnName=북구어린이도서관, htAddr=북구 산격동 120, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=3.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.9058765, " \
       "htLng=128.6159145, uCode=null, category=42, ttKind=null),HotpleVO(htId=1524, busnNum=null, " \
       "goId=ChIJMzFFN6LhZTURqw6cv7HXfiA, busnName=복현 장미공원, htAddr=북구 복현동, htAddrDet=null, htZip=null, htCont=null, " \
       "goGrd=3.9, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8933647, htLng=128.6173246, " \
       "uCode=null, category=53, ttKind=null),HotpleVO(htId=1527, busnNum=null, goId=ChIJ0daCkEThZTURbe1kYqjJnyE, " \
       "busnName=부엉이 공원, htAddr=북구 복현2동 317-1, htAddrDet=null, htZip=null, htCont=null, goGrd=5.0, htTel=null, " \
       "htImg=null, uploadPath=null, fileName=null, htLat=35.8919438, htLng=128.627141, uCode=null, category=53, " \
       "ttKind=null),HotpleVO(htId=1666, busnNum=null, goId=ChIJef3soanhZTURlj7M1gZ3cmM, busnName=커피에반하다, " \
       "htAddr=북구 산격2동 유통단지로8길 78, htAddrDet=null, htZip=null, htCont=null, goGrd=4.0, htTel=null, htImg=null, " \
       "uploadPath=null, fileName=null, htLat=35.9056086, htLng=128.6132883, uCode=null, category=10, ttKind=null)," \
       "HotpleVO(htId=1667, busnNum=null, goId=ChIJp8Y3QafhZTURHHBrdhaelCM, busnName=힐리스커피숍, htAddr=산격2동, " \
       "htAddrDet=null, htZip=null, htCont=null, goGrd=4.7, htTel=null, htImg=null, uploadPath=null, fileName=null, " \
       "htLat=35.8990946, htLng=128.6120959, uCode=null, category=10, ttKind=null),HotpleVO(htId=1759, " \
       "busnNum=3662100459, goId=null, busnName=신전떡볶이, htAddr=대구광역시 북구 복현로 35, htAddrDet=후문, htZip=41527, htCont=맛있는 " \
       "떡볶이집, goGrd=null, htTel=0539645169 , htImg=b091472b-8da9-4d36-b978-dede288ff149, uploadPath=null, " \
       "fileName=null, htLat=35.895237850112835, htLng=128.62361245541058, uCode=whdnjsdyd@naver.com/M/, category=0, " \
       "ttKind=null),HotpleVO(htId=1640, busnNum=null, goId=ChIJmeVeQ0DhZTUR3gUwgohksRE, busnName=카페멜트, htAddr=북구 복현동 " \
       "158-1, htAddrDet=null, htZip=null, htCont=null, goGrd=4.1, htTel=null, htImg=null, uploadPath=null, " \
       "fileName=null, htLat=35.899994, htLng=128.624774, uCode=null, category=10, ttKind=null),HotpleVO(htId=1645, " \
       "busnNum=null, goId=ChIJ2TkXVKjhZTURXcVGhxHQXYc, busnName=발트카페, htAddr=북구 산격2동 대불로 45, htAddrDet=null, " \
       "htZip=null, htCont=null, goGrd=4.2, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.9044258, " \
       "htLng=128.6133857, uCode=null, category=10, ttKind=null),HotpleVO(htId=1650, busnNum=null, " \
       "goId=ChIJUzzo84bhZTURbhUhiYAUHLU, busnName=핸즈커피, htAddr=북구 복현2동 복현로8길 19-36, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.4, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8971661, " \
       "htLng=128.6259975, uCode=null, category=10, ttKind=null),HotpleVO(htId=1651, busnNum=null, " \
       "goId=ChIJt-uBfaLhZTURkMP2HbJQdZI, busnName=ASO CAFE, htAddr=북구 복현동 338-29, htAddrDet=null, htZip=null, " \
       "htCont=null, goGrd=4.4, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.8928443, " \
       "htLng=128.6224459, uCode=null, category=10, ttKind=null),HotpleVO(htId=1655, busnNum=null, " \
       "goId=ChIJR0WpwKjhZTUR3qzLaKO8BeE, busnName=안카페, htAddr=북구 복현2동 94, htAddrDet=null, htZip=null, htCont=null, " \
       "goGrd=5.0, htTel=null, htImg=null, uploadPath=null, fileName=null, htLat=35.9006511, htLng=128.6218192, " \
       "uCode=null, category=10, ttKind=null)]'}"

#---------------------------------

#mbti = '{"hotples" : "zzz"}'
# print(type(mbti))
# lst = []
# for i in mbti:
#        temp = i.replace(' ','')
#        lst.append(temp)
# print(*lst)

#----------------------------------------------

mm = mbti.replace('HotpleVO','').replace('hotples','').replace(':','').replace("''",'').replace('[','').replace(']','').replace(' ','').replace('{','').replace("'",'').replace(']','').replace('),',') ')
print(mm)
lst = [mm]
print(type(lst))
print(lst[0])

lyon = (35.8964673,128.6147131)
pa = (35.8959663,128.6166937)

a = haversine(lyon,pa) * 1000
print(a)