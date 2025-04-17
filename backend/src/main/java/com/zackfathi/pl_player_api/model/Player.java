package com.zackfathi.pl_player_api.model;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDate;
import java.util.Map;

@Entity
@Table(name = "players")
@Data // includes @Getter, @Setter, @ToString, @EqualsAndHashCode
@NoArgsConstructor
@AllArgsConstructor
public class Player {

    @Id
    private String id;

    private String club;
    private String name;
    private String position;
    private String foot;

    @Column(name = "date_of_birth")
    private LocalDate dateOfBirth;

    private Integer age;
    private Integer height;

    @Column(name = "market_value")
    private Long marketValue;

    private String nationality;

    @Column(name = "image_url")
    private String imageUrl;

    @Column(columnDefinition = "jsonb")
    private String stats;

    @Column(columnDefinition = "jsonb")
    private String transfers;

    @Column(columnDefinition = "jsonb")
    private String achievements;

}
