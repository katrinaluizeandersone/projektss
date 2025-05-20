# Virtuālais ledusskapis un recepšu iepirkumu saraksta pārvaldnieks

## Projekta uzdevums

Šī projekta mērķis ir izstrādāt vienkāršu, bet efektīvu komandrindas programmu, kas ļauj lietotājam pārvaldīt pārtikas preces kas atrodas ledusskapī. Programma sniedz iespēju pievienot, noņemt un parādīt ledusskapja saturu ar attiecīgiem daudzumiem. Turklāt, izmantojot web skrāpēšanu, programma spēj iegūt recepšu sastāvdaļas no saites(www.easyhomemeals.com), attīrīt atbilstošos preču nosaukumus un izveidot iepirkumu sarakstu, kas sastāv no precēm, kas receptē ir, bet kuras ledusskapī trūkst. Šī funkcionalitāte atvieglo ēdiena gatavošanas plānošanu un iepirkšanos.

## Izmantojamās Python bibliotēkas un to iemesli

- **json**: tiek izmantota, lai saglabātu un ielādētu ledusskapja datus lokālā JSON failā, nodrošinot datu saglabāšanu starp programmas palaišanas reizēm.
- **os**: ļauj pārbaudīt vai datne (fridge_items.json) eksistē, kas nepieciešams, lai pārvaldītu datošanas saglabāšanu un ielādi.
- **re**: tiek izmantota regulārajām izteiksmēm, lai attīrītu recepšu sastāvdaļu nosaukumus no daudzumiem, mērvienībām un nevajadzīgiem aprakstiem.
- **requests**: nodrošina HTTP pieprasījumus, lai iegūtu receptes datus no interneta tīmekļa vietnēm.
- **BeautifulSoup (no bs4 moduļa)**: palīdz analizēt un izvilkt receptes sastāvdaļas no HTML lapas satura, pateicoties ērtai HTML parsēšanai.

## Savas definētas datu struktūras izmantošana

Projekta ietvaros tiek izmantota **darbība ar vārdnīcu (dictionary)** kā galvenā datu struktūra, kas pārstāv ledusskapja saturu.  
- **Vārdnīcas atslēgas** ir pārtikas preču nosaukumi (mazajiem burtiem),  
- **Vērtības** attēlo attiecīgās preces daudzumu ledusskapī.  

Šī datu struktūra nodrošina ātru piekļuvi, efektīvu preču pārvaldību (pievienošanas un noņemšanas operācijas), kā arī skaidru un strukturētu uzglabāšanu JSON formātā.  


## Programmas izmantošana

Palaižot programmu lietotājam tiek dotas 6 izvēles pirmā parāda visas lietas kuras lietoājs ir pievienojis leduskapī, otrā ļauj lietoājam pievienot produktu leduskapī trešā protams dod lietotājam noņemt produktu no saraksta. Ceturtā izvēle apvieno receptes vajadzīgos produktus salīdzina tos ar tiem kas jau atrodas leduskapī, un uztaisa sarakstu kas vēl ir jāpērk lai pagatavotu doto recepti. Piektā izvēle beidz programmas darbību, un sestā ļauj lietotājam apskatīt receptes sastāvdaļas nesalīdzinot to ar neko.

## Programmas funkcijas

- Programmā tika izveiots "Virtuāls Ledusskapis" kurš tika veidots uz hash table funkcionalitātes, tajā lauj lietotājam apskatīt,pievienot,ka arī noņemt produktus ja tas ir vajadzīgs
- Programmā ir iebūvēta webscraping funkcija ar kuras palīdzību tiek aizgūtas receptes un to sastāvdaļas.
- Programmā ir iebūvēta headers funkcija kas ļauj kodam izskatīties kā īstam pārlūkam samazinot iespēju ka kods tiks bloķēts no vajadzīgas informācijas aizgūšanas. Šis tika ielikts, jo neizmantojot šo pirmkārt tika sagādātas problēmas ar citu saitēm un nespēju aizgūt datus, kā arī šis funkcijas 0 pievienošana nodrošina ilgāku saderību ar esošo izmantoto adresi (www.easyhomemeals.com)
- Programmā tika pievienota sastāvdaļu attīrsīšana no nevajadzīgajiem pielikumiem kas nav svarīgi mūsu kodam, tas tika izdarīts definējot atslēgas vārdus piemēram 2 tablespoons no 2 tablespoons salt vai sliced no sliced beef, jo neizmantojot šo attīrīšanu veidojās problēmas ar to ka programma nespēja pilnvērtīgi salīdzināt to kas ir vajadzīgs priekš receptes un to kas atrodas ledusskapī
