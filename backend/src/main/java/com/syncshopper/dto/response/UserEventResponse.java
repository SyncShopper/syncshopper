package com.syncshopper.dto.response;

import com.syncshopper.domain.user.UserEvent;
import io.swagger.v3.oas.annotations.media.Schema;
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
@Schema(description = "User event save response")
public class UserEventResponse {

    @Schema(description = "Event ID", example = "10")
    private Long eventId;

    @Schema(description = "Product ID", example = "1")
    private Long productId;

    @Schema(description = "Recommendation ID", example = "10")
    private Long recommendationId;

    @Schema(description = "Event type", example = "PRODUCT_DETAIL_VIEW")
    private String eventType;

    @Schema(description = "Previous page before entering product detail", example = "PRODUCT_LIST")
    private String sourcePage;

    @Schema(description = "Video ID", example = "youtube-video-id")
    private String videoId;

    @Schema(description = "Category name", example = "Fashion")
    private String categoryName;

    @Schema(description = "Brand name", example = "Nike")
    private String brand;

    @Schema(description = "Event target URL")
    private String targetUrl;

    @Schema(description = "Additional event metadata as JSON")
    private String metadataJson;

    @Schema(description = "Event creation time")
    private LocalDateTime createdAt;

    public static UserEventResponse from(UserEvent userEvent) {
        return UserEventResponse.builder()
                .eventId(userEvent.getEventId())
                .productId(userEvent.getProductId())
                .recommendationId(userEvent.getRecommendationId())
                .eventType(userEvent.getEventType().name())
                .sourcePage(userEvent.getSourcePage())
                .videoId(userEvent.getVideoId())
                .categoryName(userEvent.getCategoryName())
                .brand(userEvent.getBrand())
                .targetUrl(userEvent.getTargetUrl())
                .metadataJson(userEvent.getMetadataJson())
                .createdAt(userEvent.getCreatedAt())
                .build();
    }
}
