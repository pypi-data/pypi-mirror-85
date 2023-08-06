import os
import shutil
import traceback
from time import sleep, time

import click
import toml
from லஸ்ஸியிலக்கணங்கள் import நிரல்மொழிகள்

import லஸ்ஸி


class ConfigLassi(object):
    AUTO_OPS = {
        "src": "மூலம்",
        "dist": "விநியோகம்",
        "lang": None
    }

    def __init__(self, dir_):
        ficher_config = os.path.join(dir_, 'pyproject.toml')
        self.ops = {}
        self.ops.update(self.AUTO_OPS)
        if os.path.isfile(ficher_config):
            try:
                self.ops.update(toml.load(ficher_config)['tool']['lassi'])
            except KeyError:
                pass
        for op in ['src', 'dist']:
            self.ops[op] = os.path.abspath(os.path.join(dir_, self.ops[op]))

        if not os.path.isdir(self.ops['src']):
            raise NotADirectoryError(os.path.abspath(self.ops['src']))


_dates_erreurs = {}


def obt_langue_ficher(f, probable):
    r = நிரல்மொழிகள்.நீட்சி_மூலம்_மொழி(f)
    if r:
        base, ordi, humaine = r
        if len(humaine) > 1:
            if probable in humaine:
                return ordi, probable
            print('On devine')
        return base, ordi, humaine[0]


def plus_récent(f_source, f_comp):
    if f_source in _dates_erreurs:
        return os.path.getmtime(f_source) > _dates_erreurs[f_source]
    return os.path.getmtime(f_source) > os.path.getmtime(f_comp)


def ignorer(f):
    return '__pycache__' in f or f.startswith('.')


def _recompiler(conf, forcer):
    dir_source = conf.ops["src"]
    dir_dist = conf.ops["dist"]

    for racine, dossiers, fichiers in os.walk(dir_source):
        for f in fichiers:
            f_orig = os.path.join(racine, f)
            if ignorer(f_orig):
                continue

            r = obt_langue_ficher(f, conf.ops["lang"])
            if r:
                nom_base, l_ordi, l_humaine = r
                nom_comp = nom_base + '.' + நிரல்மொழிகள்.தகவல்(l_ordi, 'நீட்சி')
                langue_cible = நிரல்மொழிகள்.தகவல்(l_ordi, 'மொழி', பதிப்பு=None)
            else:
                nom_comp = f_orig
            f_comp = dir_dist + os.path.join(racine, nom_comp)[len(dir_source):]

            doisje_recompiler = forcer or (not os.path.isfile(f_comp) or plus_récent(f_orig, f_comp))

            if doisje_recompiler:
                dir_comp = os.path.split(f_comp)[0]
                if not os.path.isdir(dir_comp):
                    os.makedirs(dir_comp)

                if r:
                    with open(f_orig, 'r', encoding='utf8') as d:
                        text_orig = d.read()
                    try:
                        print('On compile... ', f_orig)
                        if not text_orig.endswith('\n'):
                            text_orig += "\n"
                        if langue_cible != l_humaine:
                            text_comp = லஸ்ஸி.மொழியாக்கம்(
                                உரை=text_orig, நிரல்மொழி=l_ordi, மொழி=langue_cible, மூல்மொழி=l_humaine
                            )
                        else:
                            text_comp = text_orig
                        with open(f_comp, 'w', encoding='utf8') as d:
                            d.write(text_comp)
                        print('On à compilé... ', f_orig)
                        if f_orig in _dates_erreurs:
                            _dates_erreurs.pop(f_orig)
                    except Exception as e:
                        traceback.print_exc()
                        print(e)
                        _dates_erreurs[f_orig] = time()
                else:
                    shutil.copyfile(f_orig, f_comp)


@click.group()
def run():
    conf = ConfigLassi('.')
    print('வணக்கம்! என் பெயர் லஸ்ஸி.', conf.ops)


@run.command()
@click.option('--interval', default=5, help='Nombre de secondes entre recompilations.')
def observer(interval):
    conf = ConfigLassi('.')
    while True:
        _recompiler(conf, forcer=False)
        sleep(interval)


@run.command()
@click.option('--forcer/--pas-forcer', default=False)
def compiler(forcer):
    print('compiler')
    conf = ConfigLassi('.')
    _recompiler(conf, forcer)


if __name__ == '__main__':
    observer()
