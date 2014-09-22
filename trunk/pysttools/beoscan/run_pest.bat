@rem THIS IS AN EXAMPLE FILE TO IMPLEMENT BeoJACTEST in FEFLOW / FePEST
@requires PEST 13.2 opr higher (command must be adapted)

@rem -- BeoPEST preprocessing
@echo.[INFO] Running BeoJACTEST - preprocessing
@python "D:\Repositories\\red5alex.cloudforge\pyst\trunk\pysttools\beojactest\beojactest-pre.py" dam_beojactest.pst con-Sealing 100


@rem -- path
@PATH=%PATH%;C:\Program Files\PEST\;.

@rem -- run pest
@echo.[INFO] running PEST...
"C:\Program Files\PEST\beopest64_13-2.exe" "dam_beojactest.pst" /H :4052 /f < "pest.in"


@rem -- BeoPEST postprocessing
@echo.[INFO] Running BeoJACTEST - postprocessing
@python "D:\Repositories\\red5alex.cloudforge\pyst\trunk\pysttools\beojactest\beojactest-post.py" con-sealing.rrf con-sealing stabil-con-Sealing.dat
@echo.[INFO] cleaning up par files...
@del *.par
