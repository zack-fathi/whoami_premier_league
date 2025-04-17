package com.zackfathi.pl_player_api.repository;

import com.zackfathi.pl_player_api.model.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.List;

@Repository
public interface PlayerRepository extends JpaRepository<Player, String> {

    @Query("SELECT p FROM Player p " +
           "WHERE (:name IS NULL OR LOWER(p.name) LIKE LOWER(CONCAT('%', :name, '%'))) " +
           "AND (:club IS NULL OR LOWER(p.club) = LOWER(:club)) " +
           "AND (:nationality IS NULL OR LOWER(p.nationality) LIKE LOWER(CONCAT('%', :nationality, '%'))) " +
           "AND (:position IS NULL OR LOWER(p.position) = LOWER(:position))")
    List<Player> findByFilters(@Param("name") String name,
                               @Param("club") String club,
                               @Param("nationality") String nationality,
                               @Param("position") String position);
}
