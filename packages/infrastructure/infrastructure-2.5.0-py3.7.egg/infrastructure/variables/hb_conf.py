# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-29 19:01:35
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-11-09 19:52:42
from infrastructure.base.dealTime import getWeek

JAVA_COV = {
	"jacocoDir": "/home/mario/jc/lib",
	"repoDir": '/home/mario/jc/repo',
	"serviceRepoDir": '/home/mario/jc/repo/{service_name}',
	"destfileBack": '/home/mario/jc/back/{service_name}/jacoco-it-back.exec',
	"jarDir": "/home/mario/jc/{week}/{service_name}".format(week=getWeek(onlyWeek=True)),

	"destfile": "/home/mario/jc/{week}/{service_name}/destfile".format(week=getWeek(onlyWeek=True)),
	"jacocoIt" : "/home/mario/jc/{week}/{service_name}/destfile/{index}.exec".format(week=getWeek(onlyWeek=True)),
	"mergeFile": "/home/mario/jc/{week}/{service_name}/mergeFile".format(week=getWeek(onlyWeek=True)),
	"mdestfile": "/home/mario/jc/{week}/{service_name}/mdestfile".format(week=getWeek(onlyWeek=True)),
	"reportDir": "/home/mario/jc/{week}/{service_name}/report/{recordID}".format(week=getWeek(onlyWeek=True)),
	"mergeReportDir": "/home/mario/jc/{week}/{service_name}/mergeReport/{recordID}".format(week=getWeek(onlyWeek=True)),
	"copySourceDir": "/home/mario/jc/{week}/{service_name}/source".format(week=getWeek(onlyWeek=True)),	
	"restJacoco": "cd {jacocoDir};java -jar jacococli.jar dump --address {ip} --port {port} --reset --retry 3 --destfile ",
	"dumpJacoco": "cd {jacocoDir};java -jar jacococli.jar dump --address {ip} --port {port} --retry 3 --destfile "
}