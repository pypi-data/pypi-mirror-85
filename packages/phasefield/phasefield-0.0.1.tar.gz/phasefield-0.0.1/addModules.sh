git clone https://gitlab.dune-project.org/staging/dune-typetree
git clone https://gitlab.dune-project.org/staging/dune-functions
git clone https://git.imp.fu-berlin.de/agnumpde/dune-matrix-vector.git
git clone https://git.imp.fu-berlin.de/agnumpde/dune-fufem.git
git clone https://git.imp.fu-berlin.de/agnumpde/dune-solvers.git
git clone https://git.imp.fu-berlin.de/agnumpde/dune-tnnmg.git

cd dune-matrix-vector
git apply ../patches/dune-matrix-vector*.diff
cd ..
cd dune-fufem
git apply ../patches/dune-fufem*.diff
cd ..
