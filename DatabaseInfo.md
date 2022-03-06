## 数据表页

### 数据表

电影(movie)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER | 电影id, 对应豆瓣上的id |
| name | VARCHAR(200) | 电影名 |
| directors | VARCHAR(200) | 导演 |
| scenarists | VARCHAR(200) | 编剧 |
| actors | VARCHAR(400) | 演员 |
| style | VARCHAR(60) | 类型 |
| year | INTEGER | 电影年份 |
| releaseDate | VARCHAR(200) | 电影日期 |
| area | VARCHAR(200) | 制片国家/地区 |
| language | VARCHAR(60) | 语言 |
| length | INTEGER | 时长 |
| otherNames | VARCHAR(100) | 别名 |
| score | NUMERIC | 评分 |
| synopsis | TEXT | 简介 |
| imdb | VARCHAR(20) | IMDb |
| doubanUrl | VARCHAR(250) | 对应豆瓣的url |
| posterUrl | VARCHAR(250) | 电影海报路径 |
| iconUrl | VARCHAR(250) | 电影图标路径 |
| filePath | VARCHAR(250) | 电影文件路径 |
| fileUrl | VARCHAR(250) | 电影文件路径 |
| createDate | DATETIME | 电影数据创建 |
| lastWatchDate | DATETIME | 最近观看时间 |
| lastWatchUser | VARCHAR(40) | 最近观看人 |

导演,编剧, 演员(director, scenarist, actor)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(100) | 名字 |
| gender | BOOLEAN | 性别 |
| zodiac | VARCHAR(10) | 星座 |
| livingTime | VARCHAR(100) | 出生及离世时间String |
| birthday | INTEGER | 出生日期 Unix Time, the number of seconds since 1970-01-01 00:00:00 UTC.|
| leaveday | INTEGER | 离世日期 Unix Time, the number of seconds since 1970-01-01 00:00:00 UTC.|
| birthplace | VARCHAR(100) | 出生地 |
| occupation | VARCHAR(100) | 职业 |
| names_cn | VARCHAR(300) | 更多中文名 |
| names_en | VARCHAR(300) | 更多英文名 |
| family | VARCHAR(200) | 家庭成员 |
| imdb | VARCHAR(20) | IMDB编号 |
| intro | TEXT | 影人简介 |
| photoUrl | VARCHAR(200) | 头像 |


地区(area)：
>
|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(20) |  |
|`unique (name)`|

电影类型(type)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(40) |  |
|`unique (name)`|

电影标签(tag)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(40) |  |
|`unique (name)`|

电影语言(language)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(30) |  |
|`unique (name)`|

### 关系表

电影_导演(movie_director)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| director_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_director_id | FOREIGN KEY (director_id) REFERENCES director(id)|  |

电影_演员(movie_actor)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| actor_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_actor_id | FOREIGN KEY (actor_id) REFERENCES actor(id)|  |


电影_编剧(movie_scenarist)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| scenarist_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_scenarist_id | FOREIGN KEY (scenarist_id) REFERENCES scenarist(id)|  |


电影_地区(movie_area)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| area_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_area_id | FOREIGN KEY (area_id) REFERENCES area(id)|  |


电影_类型(movie_type)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| type_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_type_id | FOREIGN KEY (type_id) REFERENCES type(id)|  |


电影_标签(movie_tag)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| tag_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_tag_id | FOREIGN KEY (tag_id) REFERENCES tag(id)|  |


电影_语言(movie_language)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| movie_id | INTEGER |  |
| language_id | INTEGER |  |
| FK_movie_id | FOREIGN KEY (movie_id) REFERENCES movie(id)|  |
| FK_language_id | FOREIGN KEY (language_id) REFERENCES language(id)|  |

导演_地区(diector_area)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| diector_id | INTEGER |  |
| area_id | INTEGER |  |
| FK_diector_id | FOREIGN KEY (diector_id) REFERENCES diector(id)|  |
| FK_type_id | FOREIGN KEY (area_id) REFERENCES area(id)|  |


编剧_地区(scenarist_area)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| scenarist_id | INTEGER |  |
| area_id | INTEGER |  |
| FK_diector_id | FOREIGN KEY (scenarist_id) REFERENCES scenarist(id)|  |
| FK_type_id | FOREIGN KEY (area_id) REFERENCES area(id)|  |


演员_地区(actor_area)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| actor_id | INTEGER |  |
| area_id | INTEGER |  |
| FK_diector_id | FOREIGN KEY (actor_id) REFERENCES actor(id)|  |
| FK_type_id | FOREIGN KEY (area_id) REFERENCES area(id)|  |