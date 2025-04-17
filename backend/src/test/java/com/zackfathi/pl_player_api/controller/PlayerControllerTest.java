package com.zackfathi.pl_player_api.controller;

import com.zackfathi.pl_player_api.model.Player;
import com.zackfathi.pl_player_api.service.PlayerService;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDate;
import java.util.List;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(PlayerController.class)
class PlayerControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PlayerService playerService;

    @Test
    void testSearchPlayersWithNameReturns200() throws Exception {
        Player player = new Player("1", "Arsenal", "Saka", "RW", "Left",
        LocalDate.of(2001, 9, 5),
        22, 178, 60000000L,
        "England",
        "https://example.com/saka.jpg",
        "{}", "{}", "{}");


        Mockito.when(playerService.searchPlayers("Saka", null, null, null))
               .thenReturn(List.of(player));

        mockMvc.perform(get("/api/players?name=Saka"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$[0].name").value("Saka"));
    }
}
