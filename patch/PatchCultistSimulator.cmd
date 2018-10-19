@set CS_DIR=D:\Program Files\Steam\steamapps\common\Cultist Simulator\cultistsimulator_Data\Managed\

@set OLD_CD=%CD%
@set ASSEMBLY=Assembly-CSharp.dll
@set ASSEMBLY_MOD=MONOMODDED_%ASSEMBLY%
@set MONOMOD_DIR=MonoMod
@set PATCH_DIR=%~dp0
@set BUILD_DIR=%PATCH_DIR%\CultistSimulator.Modding.mm\bin\Release

@copy /y "%PATCH_DIR%\%MONOMOD_DIR%\*" "%BUILD_DIR%"
@cd %BUILD_DIR%
@MonoMod "%ASSEMBLY%"

@copy /y "%ASSEMBLY_MOD%" "%CS_DIR%\%ASSEMBLY%"
@copy /y "%PATCH_DIR%\%MONOMOD_DIR%\*" "%CS_DIR%"

@cd %OLD_CD%
