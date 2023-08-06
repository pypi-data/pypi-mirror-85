#! /usr/bin/python3 -i
# coding=utf-8

import os
PACKAGE_DIR=os.path.abspath(os.path.dirname(__file__))
IXAKAT2UD=os.path.join(PACKAGE_DIR,"bin","ixakat2ud")
IXAKAT2CONLL=os.path.join(PACKAGE_DIR,"bin","ixakat2conll")

import numpy
from spacy.language import Language
from spacy.symbols import LANG,NORM,LEMMA,POS,TAG,DEP,HEAD,ENT_IOB,ENT_TYPE
from spacy.tokens import Doc,Span,Token
from spacy.util import get_lang_class

class ixaKatLanguage(Language):
  lang="eu"
  max_length=10**6
  def __init__(self,convUD):
    self.Defaults.lex_attr_getters[LANG]=lambda _text:"eu"
    self.vocab=self.Defaults.create_vocab()
    self.tokenizer=ixaKatTokenizer(self.vocab,convUD)
    self.pipeline=[]
    self._meta={
      "author":"Koichi Yasuoka",
      "description":"derived from ixaKat",
      "lang":"eu_ixaKat",
      "license":"MIT",
      "name":"eu_ixaKat",
      "pipeline":"Tokenizer, POS-Tagger, Parser",
      "spacy_version":">=2.2.2"
    }
    self._path=None

class ixaKatTokenizer(object):
  to_disk=lambda self,*args,**kwargs:None
  from_disk=lambda self,*args,**kwargs:None
  to_bytes=lambda self,*args,**kwargs:None
  from_bytes=lambda self,*args,**kwargs:None
  def __init__(self,vocab,convUD):
    import subprocess
    self.model=lambda s:subprocess.check_output([IXAKAT2UD if convUD else IXAKAT2CONLL],input=s.encode("utf-8")).decode("utf-8")
    self.convUD=convUD
    self.vocab=vocab
  def __call__(self,text):
    u=self.model(text) if text else ""
    if not self.convUD:
      return u
    vs=self.vocab.strings
    r=vs.add("ROOT")
    words=[]
    lemmas=[]
    pos=[]
    tags=[]
    heads=[]
    deps=[]
    spaces=[]
    for t in u.split("\n"):
      if t=="" or t.startswith("#"):
        continue
      s=t.split("\t")
      if len(s)!=10:
        continue
      id,form,lemma,upos,xpos,dummy_feats,head,deprel,dummy_deps,misc=s
      words.append(form)
      lemmas.append(vs.add(lemma))
      pos.append(vs.add(upos))
      tags.append(vs.add(xpos))
      if deprel=="root" or deprel=="ROOT":
        heads.append(0)
        deps.append(r)
      elif head=="0":
        heads.append(0)
        deps.append(vs.add(deprel))
      else:
        heads.append(int(head)-int(id))
        deps.append(vs.add(deprel))
      spaces.append(False if "SpaceAfter=No" in misc else True)
    doc=Doc(self.vocab,words=words,spaces=spaces)
    a=numpy.array(list(zip(lemmas,pos,tags,deps,heads)),dtype="uint64")
    doc.from_array([LEMMA,POS,TAG,DEP,HEAD],a)
    doc.is_tagged=True
    doc.is_parsed=True
    return doc

def load(convUD=True):
  return ixaKatLanguage(convUD)

