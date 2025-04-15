package com.zackfathi.whoami_premier_league.repository;

import com.zackfathi.whoami_premier_league.model.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PlayerRepository extends JpaRepository<Player, String> {
}
