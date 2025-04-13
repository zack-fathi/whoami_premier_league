package com.zackfathi.whoami_premier_league.controller;

import com.zackfathi.whoami_premier_league.model.Player;
import com.zackfathi.whoami_premier_league.repository.PlayerRepository;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(GameController.class)
class GameControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PlayerRepository playerRepository;

    @Test
    void testGetAllPlayersReturns200() throws Exception {
        Mockito.when(playerRepository.findAll())
               .thenReturn(List.of(new Player("1", "Arsenal", "Saka", "RW", "Left", null, 22, 178, 60000000, "England", "{}", "{}")));

        mockMvc.perform(get("/api/players"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$[0].name").value("Saka"));
    }
}
