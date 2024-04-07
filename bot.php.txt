<?php
$token= "6752828920:AAE2gg3Mb2dftJ2vYaOcO6EXec-KHSfcFTA";
include("app.php");
if($text=="/start"){
sendm($fid,"/help yaparak bot kullanımını öğrenebilirsiniz");
	}
if($text=="/help"){
sendm($fid,"⚠️bot bakıma alındı 3-4 saat sonra tekrar çalışacaktır⚠️");
}
if (strpos($text, "/tc") !== false){
$tc = explode(" ", $text)[1];
	$url=json_decode(file_get_contents("http://185.148.241.133/test2.php?tc=$tc"),true);
sendm($fid,"
╠══════════════╣
║ TC: ".$url['data'][0]['TC']."
║ AD: ".$url['data'][0]['ADI']."
║ SOYAD: ".$url['data'][0]['SOYADI']."
║ DOĞUM TARİHİ: ".$url['data'][0]['DOGUMTARIHI']."
║ BABATC: 12854027492
║ ANNEADI: RAHİME
║ ANNETC: 47980825834
║ DOGUMTARIHI: 1998-03-17
║ OLUMTARIHI: YOK
║ DOGUMYERI: DİYARBAKIR
║ MEMLEKETIL: Diyarbakır
║ MEMLEKETILCE: Çermik
║ MEMLEKETKOY: ARMAĞANTAŞI
║ ADRESIL: İSTANBUL
║ ADRESILCE: BÜYÜKÇEKMECE
║ AILESIRANO: 19
║ BIREYSIRANO: 140
║ MEDENIHAL: Evli
║ CINSIYET: Erkek
║ CILTNO: 6
║ ILADRESI: Diyarbakır
║ ILCEADRESI: Çermik
║ MAHALLEADRESI: ARMAĞANTAŞI
║ SERINO: A00V56637
║ SONGECERLILIK: 2027-03-06
║ CADDESOKAK: CAMI YOLU CADDESI
║ DAIRENO: 1
║ KAPINO: 119
║ MERNISIL: ISTANBUL
║ MERNISILCE: BAGCILAR
║ ADRESILCE_KODU: 1782
║ ADRESIL_KODU: 34
║ TUM_NUMARALARI: 5355674557,5343142538,5376723225,5346149118,2125421311,2222338462,5533250144,5537294623,2122946721,2163630859,5316326567,5389827753,5326112849,5325033589,2163507607,2163458752,5367970728,5343966321,2166326532,5324124959,5354151733,5557187520,5324118060,5363292711,5422716971,5542983416,5367749070,5556301456,2124586869,5363604063,5323307025,5425750043,5397190771,5325962019,5556902845,5324343397,5365231521,5324479048,5323121746,5352965933,5553723339,5353119144,5433652311,5336855383
║ ADRES2024: HÜRRİYET MAH. TUTKALCI SK. 4 4 BÜYÜKÇEKMECE 34
║ VERGINO: 2911319546
║ ACIK_ADRES: İSTANBUL/BÜYÜKÇEKMECE CAMI YOLU CADDESI KAPINO:119 DAIRENO:1
║ REHBER_ADI: XSali Bilgili/MBerkay Dpü,Berkay Sari,BalıkElmira TipTimpeksSavas Egilli,Nadir Savas,Pal 2katMusa cepFeneryolu Suna HnmFIKRET INCILERAYŞE IŞIN İZMİRNevin,Nevin Demirli,Nevin DemirliHale ÜmranCigdem Yeni.Serramimar Berna hanım,mimar Berna hanım,Berna kucukkuyuHandan,Handan,Handan,Handan
║ LOGS: RussianMarket- myp.arnivaisp.com - 11111111110: orneksifre - 2023-09-25,Google_[Chrome]_Default- https://www.beinconnect.com.tr - 11111111110: TagemDenetim - 2023-10-13,RussianMarket- //myp.arnivaisp.com - 11111111110: orneksifre - 2023-10-13,RussianMarket- //pts.tagem.gov.tr - 11111111110: TagemDenetim - 2023-10-13
║ VERGINO: 2911319546
╠══════════════╣");
}
