package com.zackfathi.whoami_premier_league.model;

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

    private int age;
    private int height;

    @Column(name = "market_value")
    private long marketValue;

    private String nationality;

    @Column(columnDefinition = "jsonb")
    private String stats;  // stored as raw JSON string

    @Column(columnDefinition = "jsonb")
    private String transfers; // stored as raw JSON string
}
