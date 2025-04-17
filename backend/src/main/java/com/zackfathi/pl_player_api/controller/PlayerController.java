package com.zackfathi.pl_player_api.controller;

import com.zackfathi.pl_player_api.model.Player;
import com.zackfathi.pl_player_api.service.PlayerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/players")
public class PlayerController {

    private final PlayerService playerService;

    @Autowired
    public PlayerController(PlayerService playerService) {
        this.playerService = playerService;
    }

    @GetMapping
    public List<Player> getAllPlayers() {
        return playerService.getAllPlayers();
    }

    @GetMapping("/{id}")
    public Player getPlayerById(@PathVariable String id) {
        return playerService.getPlayerById(id);
    }

    @GetMapping("/search")
    public List<Player> searchPlayers(@RequestParam(required = false) String name,
                                      @RequestParam(required = false) String club,
                                      @RequestParam(required = false) String nationality,
                                      @RequestParam(required = false) String position) {
        return playerService.searchPlayers(name, club, nationality, position);
    }
}
