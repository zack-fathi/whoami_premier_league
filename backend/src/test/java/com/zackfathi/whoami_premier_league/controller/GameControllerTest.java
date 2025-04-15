package com.zackfathi.whoami_premier_league.controller;

import com.zackfathi.whoami_premier_league.model.Player;
import com.zackfathi.whoami_premier_league.service.GameService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDate;
import java.util.Optional;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(GameController.class)
class GameControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private GameService gameService;

    @Test
    void testStartGameReturns200() throws Exception {
        Player player = new Player("1", "Arsenal", "Saka", "RW", "Left", LocalDate.of(2001, 9, 5), 22, 178, 60000000, "England", "{}", "{}");

        Mockito.when(gameService.getRandomPlayer()).thenReturn(Optional.of(player));

        mockMvc.perform(get("/game/start/"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.name").value("Saka"));
    }
}
