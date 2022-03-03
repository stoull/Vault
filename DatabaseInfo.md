## 数据表信息

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
| birthday | REAL | 出生日期 |
| leaveday | REAL | 离世日期 |
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

电影类型(type)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(40) |  |

电影标签(tag)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(40) |  |

用户(user)：

|  字段   | 类型  | 说明  |
|  ----  | ---- | ---- |
| id | INTEGER |  |
| name | VARCHAR(20) | 名字 |
| alias | VARCHAR(20) | 别名 |
| email | VARCHAR(20) | 邮箱 |
| gender | INT | 性别 |
| phoneNumber | VARCHAR(20) | 电话号码 |
| introduction | TEXT | 绍介 |
| createDate | DATETIME | 创建日期 |