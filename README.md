#

## Instalação do Docker Desktop
https://www.docker.com/products/docker-desktop/

## Execução 

1. Start Banco de Dados  
`make database-up`  

2. Start do script de coleta de dados  
`make nba-player-loader-play`  

3. Visualizar os  logs   
`docker logs nba-player-loader -f`  