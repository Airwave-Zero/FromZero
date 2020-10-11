from mcpi.minecraft import Minecraft
from minecraftstuff import MinecraftTurtle
from mcpi import block

import mcpi
import minecraftstuff
import random


#Function to set up the initial minecraft connection to the local server

def protocol():
    mcServer = Minecraft.create("localhost", 4711)
    playerId = mcServer.getPlayerEntityId("Airwave_Zero")
    
    return (mcServer, playerId)


#Empties and clears the surrounding area near the player and replaces all blocks with air
def empty(playerInfo):
    currentPlayerPosition = playerInfo[0].entity.getPos(playerInfo[1])

    startX = currentPlayerPosition.x
    startY = currentPlayerPosition.y
    startZ = currentPlayerPosition.z

    for x in range(80):
        for y in range(80):
            for z in range(15):
                playerInfo[0].setBlock(startX + x, startY + y, startZ + z, block.AIR.id)
                playerInfo[0].setBlock(startX + x, startY + y, startZ - z, block.AIR.id)
                playerInfo[0].setBlock(startX - x, startY, startZ + z, block.AIR.id) 
                playerInfo[0].setBlock(startX + x, startY, startZ - z, block.AIR.id)
                playerInfo[0].setBlock(startX - x, startY, startZ - z, block.AIR.id)

#Creates the base track and places arches down
def create_track(playerInfo):

    currentPlayerPosition = playerInfo[0].entity.getPos(playerInfo[1])

    startX = currentPlayerPosition.x + 4
    startY = currentPlayerPosition.y
    startZ = currentPlayerPosition.z - 4


    raceParams = [] #List to hold the track information
    
    
    lavaCount = 0

    raceParams.append( ("Track boundary: Left (X, Z)", currentPlayerPosition.x + 3, currentPlayerPosition.z - 4))
    raceParams.append( ("Track boundary: Right (X, Z)", currentPlayerPosition.x + 3, currentPlayerPosition.z + 5))

    #creates the starting line
    for col in range(0, 10):
        playerInfo[0].setBlock(startX-1, startY, startZ + col, block.DIAMOND_BLOCK.id)
        if( (col == 0) or (col == 9)):
            raceParams.append( ("Starting Line Coordinates (X,Y,Z)" ,startX-1, startY, startZ + col))

    playerInfo[0].setBlock(currentPlayerPosition.x + 1, currentPlayerPosition.y-1, currentPlayerPosition.z-1, block.WATER_STATIONARY.id)
    playerInfo[0].setBlock(currentPlayerPosition.x + 1, currentPlayerPosition.y-1, currentPlayerPosition.z, block.WATER_STATIONARY.id)
    playerInfo[0].setBlock(currentPlayerPosition.x + 1, currentPlayerPosition.y-1, currentPlayerPosition.z+1, block.WATER_STATIONARY.id)

    #Creates the track

    for row in range(75):
        if(row%5 == 0):
            create_arch(playerInfo, startX, startY, startZ, row)
        playerInfo[0].setBlock(startX + row-1, startY, startZ, block.COBBLESTONE.id)
        playerInfo[0].setBlock(startX + row-1, startY+1, startZ, block.COBBLESTONE.id)
        playerInfo[0].setBlock(startX + row-1, startY+2, startZ, block.COBBLESTONE.id)
        playerInfo[0].setBlock(startX + row, startY, startZ, block.LAVA_STATIONARY.id)
        for col in range(0, 9):
            playerInfo[0].setBlock(startX + row, startY, startZ + col, block.OBSIDIAN.id)
            if( ((int(abs(startX + row)) %3 == 0) or (int(abs(startZ + col)) %2 == 0))   and (lavaCount < 250)):
                playerInfo[0].setBlock(startX + row, startY, startZ + col, block.LAVA_STATIONARY.id)
                lavaCount+=1
            if( ((int(abs(startX + row)) %11 == 0) or (int(abs(startZ + col)) %8 == 0))   and (lavaCount < 250)):
                playerInfo[0].setBlock(startX + row, startY, startZ + col, block.LAVA_STATIONARY.id)
                lavaCount+=1
                
            if(random.randint(0,8) == col):
                playerInfo[0].setBlock(startX + row, startY, startZ + col, block.LAVA_STATIONARY.id)
                              
        playerInfo[0].setBlock(startX + row, startY, startZ+8, block.LAVA_STATIONARY.id)
        playerInfo[0].setBlock(startX + row-1, startY, startZ+9, block.COBBLESTONE.id)
        playerInfo[0].setBlock(startX + row-1, startY+1, startZ+9, block.COBBLESTONE.id)
        playerInfo[0].setBlock(startX + row-1, startY+2, startZ+9, block.COBBLESTONE.id)
        

    #creates the finish line
    for col in range(0, 10):
        playerInfo[0].setBlock(startX+74, startY, startZ + col, block.DIAMOND_BLOCK.id)
        if( (col == 0) or (col == 9)):
            raceParams.append(("Finish Line Coordinates (X,Y,Z)", startX+74, startY, startZ + col))


    #return the starting line and the ending line for future usage and the left/right boundaries of the course (Track Left and Right, starting line, finish line)
    return raceParams
        

            
    
#Creates a decoration around the track using the MinecraftTurtle API and a specific block tile
def create_arch(playerInfo, turtleX, turtleY, turtleZ, archX):
    currentPlayerPosition = playerInfo[0].entity.getPos(playerInfo[1])

    skippy = MinecraftTurtle(playerInfo[0], currentPlayerPosition)
    skippy.penblock(block.SNOW_BLOCK.id,1)
    skippy.speed(10)
    
    skippy.setposition(turtleX + archX-1, turtleY, turtleZ-1)
    skippy.up(90)
    skippy.forward(8)
    skippy.down(90)
    skippy.right(90)
    skippy.forward(11)
    skippy.down(90)
    skippy.forward(8)
    skippy.up(180)
    skippy.forward(8)


#Contains the rules of the race that are constantly being checked
def race_rules(playerInfo, trackInfo):
    running = True
    while(running):
        if( playerInfo[0].getBlock(playerInfo[0].entity.getPos(playerInfo[1])) == 11): #if the player falls in lava TP to start
            playerInfo[0].postToChat("OUCH! You've fallen in lava...Quick! Jump in the water!")
            playerInfo[0].entity.setTilePos(playerInfo[1], trackInfo[2][1]-2, trackInfo[2][2], trackInfo[2][3]+5)
            
        elif (int(playerInfo[0].entity.getPos(playerInfo[1]).x) == int(trackInfo[2][1])):
            playerInfo[0].postToChat("Congratulations! You've started the obstacle course!")
            
        elif (playerInfo[0].entity.getPos(playerInfo[1]).z < trackInfo[0][2]):
            playerInfo[0].postToChat("Out of bounds! Too far left! Teleporting back to the start")
            playerInfo[0].entity.setTilePos(playerInfo[1], trackInfo[2][1]-2, trackInfo[2][2], trackInfo[2][3]+5)
            
        elif (playerInfo[0].entity.getPos(playerInfo[1]).z > trackInfo[1][2]):
            playerInfo[0].postToChat("Out of bounds! Too far right! Teleporting back to the start")
            playerInfo[0].entity.setTilePos(playerInfo[1], trackInfo[2][1]-2, trackInfo[2][2], trackInfo[2][3]+5)

        elif(playerInfo[0].entity.getPos(playerInfo[1]).x < trackInfo[2][1]-5):
            playerInfo[0].postToChat("Out of bounds! Too far back! Teleporting back to the start")
            playerInfo[0].entity.setTilePos(playerInfo[1], trackInfo[2][1]-2, trackInfo[2][2], trackInfo[2][3]+5)

        elif (playerInfo[0].entity.getPos(playerInfo[1]).x >= trackInfo[4][1]):
            playerInfo[0].postToChat("Congratulations! You've finished the obstacle course!")
            running = False
    victory_screen(playerInfo)


#The victory condition that occurs when the player crosses the finish line
def victory_screen(playerInfo):
    currentPlayerPosition = playerInfo[0].entity.getPos(playerInfo[1])

    startX = currentPlayerPosition.x 
    startY = currentPlayerPosition.y
    startZ = currentPlayerPosition.z

    for x in range(15):
        playerInfo[0].setBlock(startX+x, startY+75, startZ, block.GOLD_BLOCK.id)
        for z in range(15):
            playerInfo[0].setBlock(startX+x, startY+75, startZ+z, block.GOLD_BLOCK.id)
            
    playerInfo[0].entity.setTilePos(playerInfo[1], startX+1, startY+76, startZ+7)


        
        
    

if __name__ == "__main__":
    
    playerInfo = protocol()

    empty(playerInfo)
    trackInfo = create_track(playerInfo)
    race_rules(playerInfo, trackInfo)
    

        
