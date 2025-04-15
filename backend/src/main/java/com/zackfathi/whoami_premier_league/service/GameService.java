package com.zackfathi.whoami_premier_league.service;

import com.zackfathi.whoami_premier_league.model.Player;
import com.zackfathi.whoami_premier_league.repository.PlayerRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.Random;

@Service
public class GameService {

    private final PlayerRepository playerRepository;
    private final Random random = new Random();
    
    public GameService(PlayerRepository playerRepository) {
        this.playerRepository = playerRepository;
    }

    // get random player from db
    public Optional<Player> getRandomPlayer() {

        List<Player> allPlayers = playerRepository.findAll();
        
        // if no players
        if (allPlayers.isEmpty()) return Optional.empty();

        int index = random.nextInt(allPlayers.size());
        return Optional.of(allPlayers.get(index));

    }

    public boolean isCorrectGuess(String guess, Player player) {
        return player.getName().equalsIgnoreCase(guess.trim());
    }

    public String[] getHints(Player player) {

        return new String[] {};
    }
    
}
