package com.syncshopper.domain.user;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserEvent {

    private Long eventId;
    private Long userId;
    private Long productId;
    private Long recommendationId;
    private UserEventType eventType;
    private String sourcePage;
    private String videoId;
    private String categoryName;
    private String brand;
    private String targetUrl;
    private String metadataJson;
    private LocalDateTime createdAt;
}
