from utils.DrivenetAPI import DrivenetAPI

driveapi=DrivenetAPI(path="google_credencias.json",root_id="1O6auuYW7oJRzE9x0wISjAKBmwsqzoYUO")
print(driveapi.cd_drivenet('18mcaGuCADrItetKu09r6JBp2hk212Bu-'))
print(driveapi.ls_drivenet())