# coding: utf-8

#*****************************************************************************
# MEGUA configuration file
# https://github.com/jpedroan/megua
#
# Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

#===========
#
projectname = 'projeto'

# =====================
# SIACUA CONFIGURATION
# =====================
SIACUA_WEBKEY = "somepassword"


# =============
#
# commandline, sagews, jupyter, sagenb, ...
MEGUA_PLATFORM = "commandline"


# ===
# Directory where exercises are stored
# ===
MEGUA_EXERCISE_INPUT = os.path.join(os.getenv("HOME"),"Documents/meguainput")
if not os.path.exists(MEGUA_EXERCISE_INPUT):
    os.makedirs(MEGUA_EXERCISE_INPUT)


# ===
# Directory where graphics and results are stored
# ===
MEGUA_EXERCISES_OUTPUT = os.path.join(os.getenv("HOME"),"Downloads/meguaoutput")
if not os.path.exists(MEGUA_EXERCISES_OUTPUT):
    os.makedirs(MEGUA_EXERCISES_OUTPUT)


# ===
# Directory for CATALOGS
# ===
MEGUA_EXERCISES_CATALOG = os.path.join(os.getenv("HOME"),"Downloads/meguacatalog")
if not os.path.exists(MEGUA_EXERCISES_CATALOG):
    os.makedirs(MEGUA_EXERCISES_CATALOG)



# ===
# Language
# ===
MEGUA_SYSTEM_NATLANG = 'pt_pt'




MATHJAX_HEADER = r'''
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    extensions: ["tex2jax.js"],
    jax: ["input/TeX", "output/HTML-CSS"],
    tex2jax: {
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
      processEscapes: true
    },
    "HTML-CSS": { availableFonts: ["TeX"] }
  });
</script>
<script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'>
</script>
'''







