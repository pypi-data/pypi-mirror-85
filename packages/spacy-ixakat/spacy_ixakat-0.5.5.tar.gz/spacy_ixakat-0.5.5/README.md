[![Current PyPI packages](https://badge.fury.io/py/spacy-ixakat.svg)](https://pypi.org/project/spacy-ixakat/)

# spaCy-ixaKat

[ixaKat](http://ixa2.si.ehu.es/ixakat/ixa-pipe-dep-eu.php) wrapper for [spaCy](https://spacy.io)

## Basic Usage

```py
>>> import spacy_ixakat
>>> nlp=spacy_ixakat.load()
>>> doc=nlp("Euskaldun izatea lan extra bat izatea da.")
>>> for t in doc:
...   print("\t".join([str(t.i+1),t.orth_,t.lemma_,t.pos_,t.tag_,"_",str(0 if t.head==t else t.head.i+1),t.dep_,"_","_" if t.whitespace_ else "SpaceAfter=No"]))
...
1	Euskaldun	euskaldun	PROPN	ADJ	_	2	obl	_	_
2	izatea	izan	VERB	ADI_SIN	_	7	csubj	_	_
3	lan	lan	NOUN	IZE_ARR	_	6	obl	_	_
4	extra	extra	NOUN	ADJ	_	3	nmod	_	_
5	bat	bat	NUM	DET_DZH	_	3	nummod	_	_
6	izatea	izate	VERB	IZE_ARR	_	7	ccomp	_	_
7	da	izan	VERB	ADT	_	0	ROOT	_	SpaceAfter=No
8	.	.	PUNCT	PUNT_PUNT	_	7	punct	_	_
>>> import deplacy
>>> deplacy.render(doc)
Euskaldun PROPN <╗           obl
izatea    VERB  ═╝<══════╗   csubj
lan       NOUN  ═╗═╗<╗   ║   obl
extra     NOUN  <╝ ║ ║   ║   nmod
bat       NUM   <══╝ ║   ║   nummod
izatea    VERB  ═════╝<╗ ║   ccomp
da        VERB  ═══════╝═╝═╗ ROOT
.         PUNCT <══════════╝ punct
```

`spacy_ixakat.load(convUD=True)` loads spaCy Language pipeline for ixaKat. `convUD=False` disables the conversion into Universal Dependencies and forces the pipeline to return `str` of CoNLL.

```py
>>> import spacy_ixakat
>>> nlp=spacy_ixakat.load(convUD=False)
>>> doc=nlp("Euskaldun izatea lan extra bat izatea da.")
>>> print(doc)
1	Euskaldun	euskaldun	ADJ	ADJ	KAS=ZERO|CLUSTER=01010111|CLUSTERM=0101|ATZIZKIA=Null	2	ncmod	_	_
2	izatea	izan	ADI	ADI_SIN	KAS=ABS|ERL=KONPL|ADM=ADIZE|CLUSTER=0110100|CLUSTERM=0110|ATZIZKIA=Null	7	xcomp_subj	_	_
3	lan	lan	IZE	IZE_ARR	KAS=ZERO|CLUSTER=1011110111010|CLUSTERM=1011|ATZIZKIA=Null	6	ncmod	_	_
4	extra	extra	ADJ	ADJ	KAS=ZERO|CLUSTER=01111110100|CLUSTERM=0111|ATZIZKIA=Null	3	ncmod	_	_
5	bat	bat	DET	DET_DZH	CLUSTER=1011010|CLUSTERM=1011|ATZIZKIA=Null	3	detmod	_	_
6	izatea	izate	IZE	IZE_ARR	KAS=ABS|NUM=S|CLUSTER=0110100|CLUSTERM=0110|ATZIZKIA=a	7	ncpred	_	_
7	da	izan	ADT	ADT	ASP=PNT|MDN=A1|DADUDIO=NOR|NOR=HURA|CLUSTER=0110100|CLUSTERM=0110|ATZIZKIA=Null	0	ROOT	_	SpaceAfter=No
8	.	.	PUNT	PUNT_PUNT	_	7	PUNC	_	_


>>> import deplacy
>>> deplacy.render(doc)
Euskaldun ADJ  <╗         ncmod
izatea    ADI  ═╝<══════╗ xcomp_subj
lan       IZE  ═╗═╗<╗   ║ ncmod
extra     ADJ  <╝ ║ ║   ║ ncmod
bat       DET  <══╝ ║   ║ detmod
izatea    IZE  ═════╝<╗ ║ ncpred
da        ADT  ═╗═════╝═╝ ROOT
.         PUNT <╝         PUNC
```

## Installation for Linux (Debian, Ubuntu, Kali)

```sh
sudo apt update
sudo apt install python3-pip python3-dev default-jre-headless curl libncursesw5
pip3 install spacy_ixakat --user
```

## Installation for Linux (CentOS)

```sh
sudo yum update
sudo yum install python3-pip python3-devel java-1.8.0-openjdk-headless curl ncurses
pip3 install spacy_ixakat --user
```

## Installation for Google Colaboratory

```py
!pip install spacy_ixakat
```

Try [notebook](https://colab.research.google.com/github/KoichiYasuoka/spaCy-ixaKat/blob/master/spacy_ixakat.ipynb).

