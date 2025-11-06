
def check_winner(grid, player, to_align=5):
    """
    Vérifie si le joueur donné à aligné les 5 pions"""

    size = len(grid)

    # Vérification des lignes
    for row in range(size):
        count=0
        for col in range(size):
            if grid[row][col] == player:
                count += 1
                if count == to_align:
                    return True
            else:
                count = 0

    # Vérification des colonnes
    for col in range(size):
        count = 0
        for row in range(size):
            if grid[row][col] == player:
                count += 1
                if count == to_align:
                    return True
                else:
                    count=0

    # Vérification diagonale principale
    for r in range(size - to_align + 1):
        for c in range(size - to_align + 1):
            if all(grid[r + i][c + i] == player for i in range(to_align)):
                return True
            
    # Vérification diagonale secondaire
    for r in range(size - to_align + 1):
        for c in range(to_align - 1, size):
            if all(grid[r + i][c - i] == player for i in range(to_align)):
                return True