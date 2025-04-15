package com.zackfathi.whoami_premier_league.controller;

import org.springframework.web.bind.annotation.RestController;

import com.zackfathi.whoami_premier_league.service.GameService;
import com.zackfathi.whoami_premier_league.model.Player;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@RestController
@RequestMapping("/game")
public class GameController {

    private final GameService gameService;
    
    public GameController(GameService gameService) {
        this.gameService = gameService;
    }

    @GetMapping("/start/")
    public ResponseEntity<Player> startGame() {
        return gameService.getRandomPlayer().map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }
    
}
