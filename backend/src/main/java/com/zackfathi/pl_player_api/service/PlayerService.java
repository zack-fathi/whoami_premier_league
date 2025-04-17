package com.zackfathi.pl_player_api.service;

import com.zackfathi.pl_player_api.model.Player;
import com.zackfathi.pl_player_api.repository.PlayerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PlayerService {

    private final PlayerRepository playerRepository;

    @Autowired
    public PlayerService(PlayerRepository playerRepository) {
        this.playerRepository = playerRepository;
    }

    public List<Player> getAllPlayers() {
        return playerRepository.findAll();
    }

    public Player getPlayerById(String id) {
        return playerRepository.findById(id).orElse(null);
    }

    public List<Player> searchPlayers(String name, String club, String nationality, String position) {
        return playerRepository.findByFilters(name, club, nationality, position);
    }
}
